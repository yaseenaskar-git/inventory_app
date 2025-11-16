#!/usr/bin/env python
"""Test image upload functionality"""
import os
import sys
import django
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_app.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Inventory

# Create test user
user = User.objects.create_user(username='testuser', email='test@test.com', password='TestPass123!')
print(f"✓ Created test user: {user.username}")

# Create test inventory
inventory = Inventory.objects.create(user=user, name='Test Inventory', emoji='📦')
print(f"✓ Created test inventory: {inventory.name}")

# Create a simple test image
img = Image.new('RGB', (100, 100), color='red')
img_io = BytesIO()
img.save(img_io, format='JPEG')
img_io.seek(0)

# Login and test upload
client = Client()
logged_in = client.login(username='testuser', password='TestPass123!')
print(f"✓ Logged in: {logged_in}")

# Prepare form data
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

image_file = SimpleUploadedFile(
    "test.jpg",
    img_io.getvalue(),
    content_type="image/jpeg"
)

# Try to create an item with image
response = client.post(
    f'/accounts/inventories/{inventory.id}/items/create/',
    {
        'name': 'Test Item',
        'quantity': 5,
        'brand': 'Test Brand',
        'description': 'Test Description',
        'expiration_date': '2025-12-31',
        'image': image_file,
    }
)

print(f"Response Status: {response.status_code}")
print(f"Response Content: {response.content}")

# Check if item was created
from accounts.models import Item
items = Item.objects.filter(inventory=inventory)
if items.exists():
    item = items.first()
    print(f"✓ Item created: {item.name}")
    print(f"  - Has image: {bool(item.image)}")
    if item.image:
        print(f"  - Image path: {item.image.name}")
        print(f"  - Image URL: {item.image.url}")
else:
    print("✗ No item created")

# Cleanup
print("\nCleaning up...")
user.delete()
print("✓ Cleanup complete")
