import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction
from django.db.models import ForeignKey, ManyToManyField


class Command(BaseCommand):
    help = 'Загружает данные из JSON файла store_fixture.json в базу данных'


    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Путь к JSON файлу (по умолчанию fixtures/store_fixture.json)',
        )
        parser.add_argument(
            '--app',
            type=str,
            default='store_app',
            help='Название приложения (по умолчанию store_app)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )


    def handle(self, *args, **options):
        # Определяем путь к файлу
        if options['file']:
            file_path = options['file']
        else:
            # Ищем файл в fixtures директории приложения
            app_name = options['app']
            app_config = apps.get_app_config(app_name)
            file_path = Path(app_config.path) / 'fixtures' / 'store_fixture.json'

        # Проверяем существование файла
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл не найден: {file_path}'))
            self.stdout.write('Ищу в других местах...')

            # Попробуем найти в корне проекта
            project_root = Path(__file__).parent.parent.parent.parent
            file_path = project_root / 'store_fixture.json'

            if not os.path.exists(file_path):
                self.stderr.write(self.style.ERROR(f'Файл store_fixture.json не найден!'))
                self.stdout.write('Возможные пути:')
                self.stdout.write('1. store_app/fixtures/store_fixture.json')
                self.stdout.write('2. store_fixture.json в корне проекта')
                return

        self.stdout.write(f'Загружаю данные из файла: {file_path}')

        try:
            # Читаем JSON файл
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Проверяем структуру данных
            if not isinstance(data, list):
                self.stderr.write(self.style.ERROR('JSON должен быть массивом объектов'))
                return

            # Используем транзакцию для атомарности
            with transaction.atomic():
                # Если нужно очистить данные
                if options['clear']:
                    self.clear_existing_data(data)

                # Загружаем данные
                loaded_count = self.load_data(data)

            self.stdout.write(self.style.SUCCESS(
                f'Успешно загружено {loaded_count} записей из файла {file_path}'
            ))

        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка чтения JSON: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))
            import traceback
            traceback.print_exc()


    def clear_existing_data(self, data):
        """Очищает существующие данные для моделей из фикстуры"""
        processed_models = set()
        for item in reversed(data):
            model_name = item.get('model')
            if model_name and model_name not in processed_models:
                processed_models.add(model_name)
                try:
                    app_label, model = model_name.split('.')
                    Model = apps.get_model(app_label, model)
                    deleted_count, _ = Model.objects.all().delete()
                    self.stdout.write(f'Удалено {deleted_count} записей из {model_name}')
                except LookupError:
                    pass


    def load_data(self, data):
        """Основной метод загрузки данных"""
        loaded_count = 0

        # Проходим по данным и создаем объекты
        for item in data:
            model_name = item.get('model')
            fields = item.get('fields', {})
            pk = item.get('pk')

            if not model_name:
                continue

            try:
                # Получаем модель
                app_label, model_class_name = model_name.split('.')
                Model = apps.get_model(app_label, model_class_name)

                # Обрабатываем ForeignKey и ManyToMany поля
                processed_fields = self.process_relationships(Model, fields)

                # Создаем объект
                if pk:
                    obj, created = Model.objects.update_or_create(
                        pk=pk,
                        defaults=processed_fields
                    )
                else:
                    obj = Model.objects.create(**processed_fields)
                    created = True

                loaded_count += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f'Ошибка при создании {model_name}: {e}'
                ))
                raise

        return loaded_count


    def process_relationships(self, Model, fields):
        """Обрабатывает ForeignKey и ManyToMany отношения"""
        processed = {}

        for field_name, value in fields.items():
            try:
                # Получаем поле модели
                field = Model._meta.get_field(field_name)

                # Если это ForeignKey
                if isinstance(field, ForeignKey):
                    # value может быть ID или словарем с данными для создания
                    if isinstance(value, dict):
                        # Создаем связанный объект
                        RelatedModel = field.related_model
                        related_obj, _ = RelatedModel.objects.get_or_create(**value)
                        processed[field_name] = related_obj
                    else:
                        # Ищем существующий объект по ID
                        RelatedModel = field.related_model
                        try:
                            related_obj = RelatedModel.objects.get(pk=value)
                            processed[field_name] = related_obj
                        except RelatedModel.DoesNotExist:
                            self.stderr.write(self.style.WARNING(
                                f'Объект {field.related_model.__name__} с ID={value} не найден'
                            ))
                            processed[field_name] = None

                # Если это ManyToManyField
                elif isinstance(field, ManyToManyField):
                    # Отложим обработку ManyToMany до создания объекта
                    processed[f'_{field_name}_m2m'] = value

                # Обычное поле
                else:
                    processed[field_name] = value

            except Exception as e:
                self.stderr.write(self.style.WARNING(
                    f'Ошибка обработки поля {field_name}: {e}'
                ))
                processed[field_name] = value

        return processed