from django.db import models
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL

CATEGORIES = (
    ('P', 'Perfume'),
    ('J', 'Jewellery'),
    ('C', 'Cosmetics')
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unisex'),
)


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


class Product(models.Model):
    name = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    slug = models.SlugField(null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORIES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)
    short_description = models.TextField()
    long_description = models.TextField()
    sale = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})

    def get_add_to_favorites_url(self):
        return reverse("add-to-favorites", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item}"

    def get_sum_price(self):
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
    apartment_address = models.CharField(max_length=10, blank=True)
    phone_number = models.IntegerField()
    zip = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username


class DiscountCode(models.Model):
    code = models.CharField(max_length=15)
    discount = models.FloatField()

    def __str__(self) -> str:
        return self.code
