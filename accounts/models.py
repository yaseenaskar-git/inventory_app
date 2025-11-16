from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    """Model to represent user inventories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventories')
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=10, default='📦')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Category(models.Model):
    """User-defined categories for items."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    """An item inside an Inventory."""
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    brand = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name

    def is_low_stock(self):
        return self.quantity <= 3

    def is_expiring_soon(self):
        from django.utils import timezone
        if not self.expiration_date:
            return False
        today = timezone.localdate()
        delta = (self.expiration_date - today).days
        return delta <= 7 and delta >= 0
