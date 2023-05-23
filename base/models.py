from django.db import models
from django.urls import reverse
from django.conf import settings
import datetime
from datetime import date
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

User = settings.AUTH_USER_MODEL

CATEGORIES = (
    ('P', 'Perfume'),
    ('M', 'Makeup'),
    ('S', 'Skincare')
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unisex'),
)
MAKEUP_CATEGORY = (
    ('E', 'Eye'),
    ('F', 'Face'),
    ('L', 'Lip'),
)


class Brand(models.Model):
    brand = models.CharField(max_length=30)
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.brand

    def get_absolute_url(self):
        return reverse("brand-detail", kwargs={"slug": self.slug})


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=20, blank=True)
    favorites = models.ManyToManyField('Product', blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class PerfumeHighlights(models.Model):
    highlights = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.highlights


class SkinCareCategory(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category


class Product(models.Model):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORIES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)
    short_description = models.TextField()
    long_description = models.TextField()
    product_code = models.CharField(max_length=8)
    front_image = models.CharField(max_length=8)
    modal_details = models.TextField()
    date_added = models.DateTimeField()
    new = models.BooleanField(default=True)
    ratings = GenericRelation(Rating, related_query_name="ratings")
    highlights = models.ManyToManyField(PerfumeHighlights, blank=True)
    skincare_category = models.ForeignKey(
        SkinCareCategory, blank=True, null=True, on_delete=models.SET_NULL)
    makeup_category = models.CharField(
        max_length=10, choices=MAKEUP_CATEGORY, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})

    def get_add_to_favorites_url(self):
        return reverse("add-to-favorites", kwargs={"slug": self.slug})

    def get_remove_from_favorites_url(self):
        return reverse("remove-from-favorites", kwargs={"slug": self.slug})

    @property
    def is_new(self):
        return (datetime.datetime.today().astimezone() - self.date_added).days < 60


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item}"

    def get_sum_price(self):
        if self.item.sale_price:
            total_price = self.quantity * self.item.sale_price
        else:
            total_price = self.quantity * self.item.price
        return total_price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'DiscountCode', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} ordered {self.items}"

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_sum_price()
        if self.coupon:
            total -= self.coupon.discount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=10)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=20)
    zip = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.user.username} - st: {self.street_address} apt: {self.apartment_address} - {self.city} {self.zip}. Phone {self.phone_number}"


class DiscountCode(models.Model):
    code = models.CharField(max_length=15)
    discount = models.FloatField()

    def __str__(self) -> str:
        return self.code


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author} - {self.product.name} ({self.product.short_description})"
