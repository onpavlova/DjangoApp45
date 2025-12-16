from django import forms
from django.core.exceptions import ValidationError

from store_app.models import Product


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label="Наименование",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование'}),
    )
    description = forms.CharField(
        label='Содержание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'row': 5, 'placeholder': 'Введите описание товара'}),

    )
    price = forms.DecimalField(
        min_value=0,
        label='Цена',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите цену товара'}),

    )


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'price': 'Цена',
            'category': 'Категория',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'row': 5, 'placeholder': 'Введите описание товара'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean_name(self):
        """Кастомная валидация name."""
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise ValidationError('Заголовок должен содержать минимум 5 символов')
        return name


    def clean_price(self):
        """Кастомная валидация price."""
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена должна быть положительной')
        return price


class ProductDeleteForm(forms.Form):
    """Форма для подтверждения удаления товара."""
    confirm = forms.BooleanField(
        required=True,
        label='Подтвердите удаление',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
