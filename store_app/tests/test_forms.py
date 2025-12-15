import pytest
from store_app.models import Product, Category
from store_app.forms import ProductForm, ProductModelForm, ProductDeleteForm


@pytest.mark.django_db
def test_product_form_valid():
    """Проверка валидации ProductForm"""
    form_data = {
        'name': 'Тестовый товар',
        'description':'Описание тестового товара',
        'price': 100,
    }
    form = ProductForm(data=form_data)

    assert form.is_valid()

    clean_data = form.cleaned_data
    assert clean_data['name'] == form_data['name']


@pytest.mark.django_db
def test_productmodalform_valid(category_1):
    """Проверка валидации ProductModalForm"""
    form_data = {
        'name': 'Тестовый товар',
        'description':'Описание тестового товара',
        'price': 100,
        'category': category_1,
    }
    form = ProductModelForm(data=form_data)

    assert form.is_valid()

@pytest.mark.django_db
def test_productmodalform_valid_negative(category_1):
    """Проверка валидации ProductModalForm"""
    form_data = {
        'name': 'Тестовый товар',
        'description':'Описание тестового товара',
        'price': -100,
        'category': category_1,
    }
    form = ProductModelForm(data=form_data)

    assert not form.is_valid()