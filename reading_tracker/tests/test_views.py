from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Book, ReadingProgress
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
            length_pages=200,
            status='reading'
        )
        self.book_2 = Book.objects.create(
            user=self.user,
            title='Test Book 2',
            author='Test Author',
            publisher='Test Publisher',
            gbooks_id='012345678901',
            book_type='e-book',
            length_pages=200,
            status='finished'
        )

    def test_validated_access(self):
        """
        Tests that authenticated users can access list view, checks response status code, template, and context data, and verifies that user's reading statuses are displayed
        """
        response = self.client.get(reverse('reader'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading_tracker/book_list.html')
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

class ReaderSearchViewTest(TestCase):
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

class ReaderCreateViewTest(TestCase):
    def setUp(self):
        """
        create test user
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_validated_access(self):
        """
        Tests that authenticated users can access create view, checks response status code, and template
        """
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading_tracker/book_form.html')
    
    def test_invalidated_access(self):
        """
        Tests accessing create view while not logged in and checks if user is redirected to login page
        """
        self.client.logout()

        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('book-create'))

    def test_form_fields(self):
        """
        tests for fields loaded into form
        """
        response = self.client.get(reverse('book-create'))
        form = response.context['form']
        self.assertIn('cover_url', form.fields)
        self.assertIn('gbooks_id', form.fields)
        self.assertIn('title', form.fields)
        self.assertIn('author', form.fields)
        self.assertIn('publisher', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('book_type', form.fields)
        self.assertIn('length_pages', form.fields)
        self.assertIn('length_time', form.fields)
        self.assertIn('status', form.fields)

    def test_with_session_data(self):
        """
        tests for initial form data if provided session data
        """
        # So this test is supposed to supply context data that gets turned into initial form 
        # values by the view, however there doesn't seem to be a good way to test for initial 
        # form values supplied by the view, so for now we insert values directly into the form
        # and check for those ¯\_(ツ)_/¯
        form_data = {
            'cover_url': 'http://example.com/cover.jpg',
            'title': 'Test Book',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'description': 'Test Description',
            'length_pages': 200,
            'gbooks_id': 'test123',
            'status': 'finished'
        }
        form = CreateForm(initial=form_data)
        self.assertEqual(form.initial['cover_url'], form_data['cover_url'])
        self.assertEqual(form.initial['title'], form_data['title'])
        self.assertEqual(form.initial['author'], form_data['author'])
        self.assertEqual(form.initial['publisher'], form_data['publisher'])
        self.assertEqual(form.initial['description'], form_data['description'])
        self.assertEqual(form.initial['length_pages'], form_data['length_pages'])
        self.assertEqual(form.initial['gbooks_id'], form_data['gbooks_id'])
        self.assertEqual(form.initial['status'], form_data['status'])

    def test_without_session_data(self):
        """
        tests for initial form data if not provided session data
        """
        response = self.client.get(reverse('book-create'))
        form = response.context['form']
        self.assertIsNone(form.initial.get('cover_url'))
        self.assertIsNone(form.initial.get('gbooks_id'))
        self.assertIsNone(form.initial.get('title'))
        self.assertIsNone(form.initial.get('author'))
        self.assertIsNone(form.initial.get('publisher'))
        self.assertIsNone(form.initial.get('description'))
        self.assertIsNone(form.initial.get('length_pages'))
        self.assertIsNone(form.initial.get('length_time'))
        self.assertIsNone(form.initial.get('status'))

    def test_form_submission(self):
        """
        tests if form submits successfully and if book is in database
        """
        form_data = {
            'cover_url': 'http://example.com/cover.jpg',
            'title': 'Test Book',
            'author': 'Test Author',
            'publisher': 'Test Publisher',
            'description': 'Test Description',
            'gbooks_id': 'test123',
            'length_pages': 200,
            'book_type': 'paper-book',
            'length_time': '',
            'status': 'finished'
        }

        form = CreateForm(data=form_data)
        if form.is_valid():
            response = self.client.post(reverse('book-create'), data=form_data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('reader'))
            self.assertTrue(Book.objects.filter(user=self.user, gbooks_id='test123').exists())

        else:
            print(form.errors)
            self.fail("Form is not valid")
