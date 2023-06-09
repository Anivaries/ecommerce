from django.contrib import admin
from .models import Product, Order, OrderItem, BillingAddress, UserProfile, DiscountCode, Brand, PerfumeHighlights, SkinCareCategory, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    list_display = ["name", "short_description", "size"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "total_price"]

    def total_price(self, instance):
        return instance.get_total_price()


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street_address")


admin.site.register(Comment)
admin.site.register(SkinCareCategory)
admin.site.register(PerfumeHighlights)
admin.site.register(Brand)
admin.site.register(DiscountCode)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(BillingAddress, BillingAddressAdmin)
