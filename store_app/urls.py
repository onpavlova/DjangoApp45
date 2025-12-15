from django.urls import path
from .views import about
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, IndexTemplateView


urlpatterns = [
    path('',IndexTemplateView.as_view(), name='index'),
    path('about/',about, name='about'),
    path('products/',ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/',ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]