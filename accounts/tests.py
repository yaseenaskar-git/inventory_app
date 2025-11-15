from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.dashboard_url = reverse('dashboard')

    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_register_user_success(self):
        data = {
            'email': 'testuser@example.com',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='TestPass123!')
        data = {
            'email': 'test@example.com',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Form error, no redirect

    def test_register_password_mismatch(self):
        data = {
            'email': 'newuser@example.com',
            'password1': 'SecurePassword123!',
            'password2': 'DifferentPassword123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='TestPass123!')
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'WrongPassword123!',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Form shows error

    def test_dashboard_requires_authentication(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_accessible_when_authenticated(self):
        user = User.objects.create_user(username='test@example.com', email='test@example.com', password='TestPass123!')
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_logout(self):
        user = User.objects.create_user(username='test@example.com', email='test@example.com', password='TestPass123!')
        self.client.login(username='test@example.com', password='TestPass123!')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
