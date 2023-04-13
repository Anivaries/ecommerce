from django.urls import path
from .views import ProductDetailView, ProductListView, add_to_cart, remove_from_cart, OrderSummaryView, remove_item_from_cart, CheckoutView, contact_form, add_to_favorites, IndexPageView, UserProfileView, update_profile, show_favorites, CouponView, empty_cart, list_by_female_products, list_by_male_products, BrandView, BrandDetail, get_perfumes

urlpatterns = [
    path('', IndexPageView.as_view(), name='index-page'),
    path('products/', ProductListView.as_view(), name="product-list"),
    path('products/<slug:slug>', ProductDetailView.as_view(), name="product-detail"),
    path('brand-list/', BrandView.as_view(), name='brand-list'),
    path('brand/<slug:slug>', BrandDetail.as_view(), name="brand-detail"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('apply-coupon/', CouponView.as_view(), name='apply-coupon'),
    path('contact/', contact_form, name='contact'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug:slug>/',
         remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug:slug>/',
         remove_item_from_cart, name="remove-item-from-cart"),
    path('add-to-favorites/<slug:slug>/',
         add_to_favorites, name="add-to-favorites"),
    path('update-profile/', update_profile, name="profile-update"),
    path('favorites/', show_favorites, name="favorites"),
    path('empty-cart', empty_cart, name="empty-cart"),
    path('female_perfumes/', list_by_female_products, name="female-perfumes"),
    path('male_perfumes/', list_by_male_products, name="male-perfumes"),
    path('perfumes/', get_perfumes, name="perfumes"),
]
