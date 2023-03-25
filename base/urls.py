from django.urls import path
from .views import ProductDetailView, ProductListView, add_to_cart, remove_from_cart, OrderSummaryView, remove_item_from_cart, CheckoutView


urlpatterns = [
    path('products/', ProductListView.as_view(), name="product-list"),
    path('products/<slug:slug>', ProductDetailView.as_view(), name="product-detail"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('add-to-cart/<slug:slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug:slug>/',
         remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug:slug>/',
         remove_item_from_cart, name="remove-item-from-cart"),
]
