from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # <- this is the new field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


# Optional helper to create some demo products quickly
def create_sample_products():
    if Product.objects.exists():
        return
    Product.objects.create(
        name="Minimalist Desk Lamp",
        description="Soft warm light for your workspace.",
        price=3499.00,
        stock=15,
    )
    Product.objects.create(
        name="Comfort Office Chair",
        description="Ergonomic chair with breathable mesh.",
        price=18999.00,
        stock=7,
    )
    Product.objects.create(
        name="Wireless Speaker",
        description="Compact speaker with rich sound.",
        price=5999.00,
        stock=10,
    )
    Product.objects.create(
        name="Ceramic Coffee Mug",
        description="Simple matte mug for everyday use.",
        price=1299.00,
        stock=0,
    )
