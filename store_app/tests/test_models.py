from decimal import Decimal

import pytest
from store_app.models import Product, Category
from store_app.tests.conftest import product_2


@pytest.mark.django_db
def test_category_create(category_1):
    assert Category.objects.count() == 1
    assert category_1.name == 'Рукоделие'


@pytest.mark.django_db
def test_product_create(product_1, product_2):
    assert Product.objects.count() == 2
    assert product_1.name == 'Вышивка Телефон'
    assert product_2.price == 3000


@pytest.mark.django_db
def test_create_read_update_delete_product():
    """Тест полного цикла CRUD для Product"""
    # Создаем категорию для теста
    category = Category.objects.create(name='Тестовая категория')

    # CREATE
    product = Product.objects.create(
        name='Тестовый товар',
        description='Описание тестового товара',
        price=Decimal('99.99'),
        category=category
    )
    product_id = product.id

    # READ
    retrieved_product = Product.objects.get(id=product_id)
    assert retrieved_product.name == 'Тестовый товар'
    assert retrieved_product.price == Decimal('99.99')
    assert retrieved_product.category == category

    # UPDATE
    retrieved_product.name = 'Обновленный товар'
    retrieved_product.price = Decimal('149.99')
    retrieved_product.save()

    updated_product = Product.objects.get(id=product_id)
    assert updated_product.name == 'Обновленный товар'
    assert updated_product.price == Decimal('149.99')

    # DELETE
    deleted_count, _ = Product.objects.filter(id=product_id).delete()
    assert deleted_count > 0

    # Проверяем, что товар удален
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product_id)

    # Категория должна остаться (SET_NULL поведение не применяется при удалении товара)
    assert Category.objects.filter(id=category.id).exists()