from celery import shared_task
import time
import logging
from .models import Product

# Создаем логгер для задач
logger = logging.getLogger(__name__)


@shared_task
def log_new_product(product_id):
    """
    Асинхронная задача для логирования информации о новом товаре.
    """
    logger.info("Task STARTED for product_id: %s", product_id)
    try:
        product = Product.objects.get(id=product_id)
        log_message = (
            f"НОВЫЙ ТОВАР СОЗДАН | "
            f"ID: {product.id} | "
            f"Название: {product.name} | "
            f"Цена: {product.price} | "
            f"Категория: {product.category.name if product.category else 'Не указана'} | "
            f"Дата создания: {product.created_at}"
        )
        # Логируем сообщение
        logger.info(log_message)
        # Для наглядности также выводим в консоль
        print(f"[Celery Task] {log_message}")
        return f"Успешно залогирован товар '{product.name}'"
    except Product.DoesNotExist:
        error_msg = f"Задача log_new_product: Товар с ID={product_id} не найден."
        logger.error(error_msg)
        return error_msg
