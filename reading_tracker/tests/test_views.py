from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse



class ReaderLoginViewTest(TestCase):
    def test_login_template(self):
        """
        Ensure the login url return the right template
        """
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'reading_tracker/login.html')

    def test_login_validation(self):
        """
        Ensure a valid login redirects to list template
        """
        User.objects.create_user(username='testuser', password='testpassword')

        response = self.client.post(reverse('login'), {'username':'testuser', 'password':'testpassword'})

        self.assertRedirects(response, reverse('reader'))

    def test_login_invalidation(self):
        """
        Ensure an invalid login does not redirect to list template
        """
        response = self.client.post(reverse('login'), {'username':'testuser', 'password':'testpassword'})

        self.assertEqual(response.status_code, 200)

    def test_valid_redirection(self):
        """
        Ensures that a valid user is redirected to reader template when accessing login url again
        """
        User.objects.create_user(username='testuser', password='testpassword')

        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('login'))

        self.assertRedirects(response, reverse('reader'))

class ReaderRegisterViewTest(TestCase):
    def test_register_template(self):
        """
        Ensure register url returns correct template
        """
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'reading_tracker/register.html')
    
    def test_register_validation(self):
        """
        Tests user registration with valid data and checks for successful registration, user existence, and authentication
        """
        response = self.client.post(reverse('register'), {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'testpassword'
        })

        self.assertRedirects(response, reverse('reader'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

        authenticated_user = authenticate(username='testuser', password='testpassword')
        self.assertIsNotNone(authenticated_user)
        self.assertTrue(authenticated_user.is_authenticated)

    def test_register_invalidation(self):
        """
        Tests user registration with invalid data
        """
        response = self.client.post(reverse('register'), {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'youjustlostthegame'
        })

        self.assertEqual(response.status_code, 200)

    def test_valid_redirection(self):
        """
        Ensures authenticated users are redirected to reader template when trying to access register view
        """
        User.objects.create_user(username='testuser', password='testpassword')

        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('register'))

        self.assertRedirects(response, reverse('reader'))