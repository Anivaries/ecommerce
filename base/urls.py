from django.urls import path
from .views import ProductDetailView, ProductListView, add_to_cart, remove_from_cart, OrderSummaryView, remove_item_from_cart, CheckoutView, contact_form, add_to_favorites, remove_from_favorites, IndexPageView, UserProfileView, update_profile, show_favorites, CouponView, empty_cart, list_by_female_perfumes, list_by_male_perfumes, BrandView, BrandDetail, get_perfumes, get_new_perfumes, arrange_by_rating_perfumes, get_skincare, get_skincare_moisturizers, get_skincare_lip_balm, get_new_skincare, arrange_by_rating_skincare, get_skincare_cleanser, get_skincare_masks, get_makeup, get_new_makeup, get_makeup_eye, get_makeup_face, get_makeup_lip, arrange_by_rating_makeup, get_all_new_products, get_makeup_by_brand, get_perfumes_by_brand, get_skincare_by_brand, delete_comment, page_not_found, all_brands_s, all_brands_p, all_brands_m, items_on_sale, perfumes_on_sale, makeup_on_sale, skincare_on_sale, OrdersListView

#

urlpatterns = [
    path('404/', page_not_found, name='page-not-found'),
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
    path('delete-comment/<int:pk>/',
         delete_comment, name='delete-comment'),
    path('update-comment/<int:pk>/',
         ProductDetailView.update, name='update-comment'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug:slug>/',
         remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug:slug>/',
         remove_item_from_cart, name="remove-item-from-cart"),
    path('add-to-favorites/<slug:slug>/',
         add_to_favorites, name="add-to-favorites"),
    path('remove-from-favorites/<slug:slug>/',
         remove_from_favorites, name="remove-from-favorites"),
    path('update-profile/', update_profile, name="profile-update"),
    path('favorites/', show_favorites, name="favorites"),
    path('empty-cart', empty_cart, name="empty-cart"),
    path('female-perfumes/', list_by_female_perfumes, name="female-perfumes"),
    path('male-perfumes/', list_by_male_perfumes, name="male-perfumes"),
    path('perfumes/', get_perfumes, name="perfumes"),
    path('makeup/', get_makeup, name="makeup"),
    path('eye-makeup/', get_makeup_eye, name="eye-makeup"),
    path('ace-makeup/', get_makeup_face, name="face-makeup"),
    path('lip-makeup/', get_makeup_lip, name="lip-makeup"),
    path('skincare/', get_skincare, name="skincare"),
    path('skincare/moisturizers/', get_skincare_moisturizers, name="moisturizers"),
    path('skincare/lip-balm-care/', get_skincare_lip_balm, name="lipbalm"),
    path('skincare/cleansers/', get_skincare_cleanser, name="cleanser"),
    path('skincare/masks/', get_skincare_masks, name="masks"),
    path('new-perfumes/', get_new_perfumes, name="new-perfumes"),
    path('new-makeup/', get_new_makeup, name="new-makeup"),
    path('new-arrivals/', get_all_new_products, name="new-arrivals"),
    path('new-skincare/', get_new_skincare, name="new-skincare"),
    path('top-perfumes/', arrange_by_rating_perfumes, name="top-perfumes"),
    path('top-skincare/', arrange_by_rating_skincare, name="top-skincare"),
    path('brands/skincare/', all_brands_s, name="brands-by-s"),
    path('brands/makeup/', all_brands_m, name="brands-by-m"),
    path('brands/perfumes/', all_brands_p, name="brands-by-p"),
    path('top-makeup/', arrange_by_rating_makeup, name="top-makeup"),
    path('brand/<slug:slug>/makeup/', get_makeup_by_brand, name="makeup-by-brand"),
    path('brand/<slug:slug>/skincare/',
         get_skincare_by_brand, name="skincare-by-brand"),
    path('brand/<slug:slug>/perfumes/',
         get_perfumes_by_brand, name="perfumes-by-brand"),
    path('sale/', items_on_sale, name="items_on_sale"),
    path('perfumes/sale/', perfumes_on_sale, name="perfumes_on_sale"),
    path('makeup/sale/', makeup_on_sale, name="makeup_on_sale"),
    path('skincare/sale/', skincare_on_sale, name="skincare_on_sale"),
    path('orders/', OrdersListView.as_view(), name="orders"),

]
