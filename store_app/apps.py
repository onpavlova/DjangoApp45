from django.apps import AppConfig


class StoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_app'

    def ready(self):
        """
        Метод ready вызывается при загрузке приложения.
        Здесь импортируем и регистрируем сигналы.
        """
        import store_app.signals
