from django.test import TestCase
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