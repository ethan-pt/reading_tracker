from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Book

from datetime import timedelta



class BookModelTest(TestCase):
    def setUp(self):
        """
        Create generic test book
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            user=self.user,
            gbooks_id='123456789012',
            title='Test Book',
            author='Test Author',
            book_type='paper-book',
            status='reading'
        )
    
    def test_book_creation(self):
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.book_type, 'paper-book')
        self.assertEqual(self.book.status, 'reading')
    
    def test_current_page_default(self):
        self.assertEqual(self.book.current_page, 0)

    def test_current_time_default(self):
        self.assertEqual(self.book.current_time, timedelta(0))

    def test_last_updated(self):
        old_last_updated = self.book.last_updated
        self.book.title = 'Updated Title'
        self.book.save()
        new_last_updated = Book.objects.get(id=self.book.id).last_updated
        self.assertNotEqual(old_last_updated, new_last_updated)

    def test_unique_gbooks_id(self):
        duplicate_book = Book(
            user=self.user,
            gbooks_id='123456789012',
            title='Duplicate Test Book',
            author='Duplicate Test Author',
            book_type='paper-book',
            status='reading'
        )

        with self.assertRaises(Exception) as context:
            duplicate_book.save()
        self.assertTrue('unique' in str(context.exception))
