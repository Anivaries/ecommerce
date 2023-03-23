from django.urls import path
from .views import ProductDetailView, ProductListView, add_to_cart, remove_from_cart


urlpatterns = [
    path('products/', ProductListView.as_view(), name="product-list"),
    path('products/<slug:slug>', ProductDetailView.as_view(), name="product-detail"),
    path('add-to-cart/<slug:slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug:slug>/',
         remove_from_cart, name="remove-from-cart"),
]
