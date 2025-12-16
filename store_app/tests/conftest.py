import pytest
from store_app.models import Product, Category

@pytest.fixture
def category_1():
    return Category.objects.create(
        name='Рукоделие',
        description='Содержит товары вязания, вышивки и др'
    )


@pytest.fixture
def product_1(category_1):
    return Product.objects.create(
        name='Вышивка Телефон',
        description='Вышивка красивой картины',
        price=1599,
        category=category_1
    )


@pytest.fixture
def product_2(category_1):
    return Product.objects.create(
        name='Акриловые краски',
        description='Краски по ткани 15 цветов',
        price=3000,
        category=category_1
    )

