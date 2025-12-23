from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import log_new_product

@receiver(post_save, sender=Product)
def trigger_product_logging(sender, instance, created, **kwargs):
    """
    Обработчик сигнала post_save для модели Product.
    Запускает асинхронную задачу логирования, если товар был создан (а не обновлен).
    """
    if created:  # Важно: запускаем задачу только для новых записей
        # Передаем задаче ID созданного товара
        log_new_product.delay(instance.id)
        # .delay() - это Celery-метод для асинхронного вызова задачи