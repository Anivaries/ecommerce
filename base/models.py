from django.db import models
from django.urls import reverse
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} ordered {self.items}"
