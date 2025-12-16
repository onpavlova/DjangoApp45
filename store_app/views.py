from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm, ProductModelForm, ProductDeleteForm


class IndexTemplateView(TemplateView):
    template_name = "store_app/index.html"

def about(request):
    """Страница о нас."""
    return HttpResponse('<h1>About us!</h1>')


class ProductListView(ListView):
    "CBV для товаров"
    model = Product
    template_name = 'store_app/product_list.html'
    context_object_name = 'products'
    # paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список товаров'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store_app/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    template_name = 'store_app/product_add.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании поста."""
        messages.success(self.request, 'Товар успешно создан')
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'store_app/product_edit.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании поста."""
        messages.success(self.request, 'Товар успешно обновлен')
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store_app/product_delete.html'
    success_url = reverse_lazy('product_list')



