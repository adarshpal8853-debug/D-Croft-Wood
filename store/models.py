from django.db import models


class Product(models.Model):

    name = models.CharField(
        max_length=100
    )

    price = models.IntegerField()

    description = models.TextField()

    image = models.ImageField(
        upload_to='products/'
    )

    category = models.CharField(
        max_length=50,
        default="Furniture"
    )

    material = models.CharField(
        max_length=100,
        default="Wood"
    )

    dimensions = models.CharField(
        max_length=100,
        default="Standard Size"
    )

    def __str__(self):
        return self.name



class Cart(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(
        default=1
    )

    def __str__(self):

        return self.product.name



class Wishlist(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    def __str__(self):

        return self.product.name


class Order(models.Model):

    name = models.CharField(max_length=100)

    product = models.TextField(
        null=True,
        blank=True
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=15
    )

    total_price = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone=models.CharField(
        max_length=15
    )

    address=models.TextField()

    def __str__(self):

        return self.user.username
  