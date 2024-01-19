from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Book, ReadingStatus, ReadingProgress
from ..forms import CreateForm



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

class ReaderListViewTest(TestCase):
    def setUp(self):
        """
        Create test user, books, and reading statuses
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.book_1 = Book.objects.create(
            user=self.user,
            title='Test Book 1',
            author='Test Author',
            publisher='Test Publisher',
            gbooks_id='123456789012',
            book_type='paper-book',
            length_pages=200
        )
        self.book_2 = Book.objects.create(
            user=self.user,
            title='Test Book 2',
            author='Test Author',
            publisher='Test Publisher',
            gbooks_id='012345678901',
            book_type='e-book'
        )
        
        self.reading_status_1 = ReadingStatus.objects.create(
            user=self.user,
            book=self.book_1,
            status='reading'
        )
        self.reading_status_2 = ReadingStatus.objects.create(
            user=self.user,
            book=self.book_2,
            status='finished'
        )

    def test_validated_access(self):
        """
        Tests that authenticated users can access list view, checks response status code, template, and context data, and verifies that user's reading statuses are displayed
        """
        response = self.client.get(reverse('reader'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading_tracker/readingstatus_list.html')
        self.assertIn('books', response.context)
        self.assertContains(response, 'Test Book 1')
        self.assertContains(response, 'Test Book 2')

    def test_invalidated_access(self):
        """
        Tests accessing reader view while not logged in and checks if user is redirected to login page
        """
        self.client.logout()

        response = self.client.get(reverse('reader'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('reader'))

class ReaderSearchView(TestCase):
    def setUp(self):
        """
        create test user
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_validated_access(self):
        """
        Tests that authenticated users can access list view, checks response status code, and template
        """
        response = self.client.get(reverse('book-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading_tracker/book_search.html')

    def test_invalidated_access(self):
        """
        Tests accessing search view while not logged in and checks if user is redirected to login page
        """
        self.client.logout()

        response = self.client.get(reverse('book-search'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('book-search'))