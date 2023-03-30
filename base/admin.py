from django.contrib import admin
from .models import Product, Order, OrderItem, BillingAddress, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "size")


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user"]


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street_address")


# admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(BillingAddress, BillingAddressAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
