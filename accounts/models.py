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
