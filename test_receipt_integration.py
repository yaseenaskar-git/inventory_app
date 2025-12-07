#!/usr/bin/env python
"""
Quick integration test for Receipt Gallery feature
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_app.settings')
sys.path.insert(0, str(Path(__file__).parent))

django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Inventory, Receipt
from datetime import date
import json


class ReceiptGalleryIntegrationTests(TestCase):
    """Test Receipt Gallery feature"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.inventory = Inventory.objects.create(
            name='Kitchen',
            emoji='🍳',
            user=self.user
        )
        self.client.login(username='testuser', password='TestPass123!')

    def test_receipt_gallery_page_loads(self):
        """Test that receipt gallery page loads"""
        url = reverse('receipt_gallery', args=[self.inventory.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/receipt_gallery.html')

    def test_create_receipt_without_image(self):
        """Test creating receipt without image"""
        url = reverse('create_receipt', args=[self.inventory.id])
        data = {
            'name': 'Office Supplies',
            'date': str(date.today()),
            'description': 'Monthly office supplies purchase'
        }
        response = self.client.post(url, data=data)
        result = response.json()
        
        self.assertTrue(result['success'])
        self.assertTrue(Receipt.objects.filter(name='Office Supplies').exists())
        receipt = Receipt.objects.get(name='Office Supplies')
        self.assertEqual(receipt.inventory, self.inventory)

    def test_create_receipt_without_name_fails(self):
        """Test that creating receipt without name fails"""
        url = reverse('create_receipt', args=[self.inventory.id])
        data = {
            'name': '',  # Missing name
            'date': str(date.today()),
            'description': 'Monthly supplies'
        }
        response = self.client.post(url, data=data)
        result = response.json()
        
        self.assertFalse(result['success'])
        self.assertIn('name is required', result['error'].lower())

    def test_create_receipt_without_date_fails(self):
        """Test that creating receipt without date fails"""
        url = reverse('create_receipt', args=[self.inventory.id])
        data = {
            'name': 'Office Supplies',
            'date': '',  # Missing date
            'description': 'Monthly supplies'
        }
        response = self.client.post(url, data=data)
        result = response.json()
        
        self.assertFalse(result['success'])
        self.assertIn('date is required', result['error'].lower())

    def test_delete_receipt(self):
        """Test deleting a receipt"""
        receipt = Receipt.objects.create(
            inventory=self.inventory,
            name='Test Receipt',
            date=date.today(),
            description='Test'
        )
        url = reverse('delete_receipt', args=[self.inventory.id, receipt.id])
        response = self.client.post(url, data={})
        result = response.json()
        
        self.assertTrue(result['success'])
        self.assertFalse(Receipt.objects.filter(id=receipt.id).exists())

    def test_user_cannot_access_other_users_receipts(self):
        """Test that users can't access other users' receipts"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='OtherPass123!'
        )
        other_inventory = Inventory.objects.create(
            name='Other Kitchen',
            emoji='🍴',
            user=other_user
        )
        
        # Try to access another user's receipt gallery
        url = reverse('receipt_gallery', args=[other_inventory.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    import unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ReceiptGalleryIntegrationTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
