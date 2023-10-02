from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Book, ReadingStatus, ReadingProgress

from datetime import timedelta



class BookModelTest(TestCase):
    def setUp(self):
        """
        Create generic test book
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            isbn='1234567890123',
        )

    def test_create_paper_book(self):
        """
        Configure paper book options, ensure info is stored properly
        """
        book = self.book
        book.book_type = 'paper-book'
        book.length_pages = 200

        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'paper-book')
        self.assertEqual(book.length_pages, 200)
        self.assertIsNone(book.length_time)

    def test_create_ebook(self):
        """
        Configure e-book options, ensure info is stored properly
        """
        book = self.book
        book.book_type = 'e-book'

        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'e-book')
        self.assertIsNone(book.length_pages)
        self.assertIsNone(book.length_time)

    def test_create_audio_book(self):
        """
        Configure audio book options, ensure info is stored properly
        """
        book = self.book
        book.book_type = 'audio-book'
        book.length_time = timedelta(
            hours=2,
            minutes=30,
        )

        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'audio-book')
        self.assertEqual(book.length_time.total_seconds(), 9000)
        self.assertIsNone(book.length_pages)

class ReadingStatusTest(TestCase):
    def setUp(self):
        """
        Create generic test user, book, and reading status
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            isbn='1234567890123',
            book_type='paper-book',
            length_pages=200
        )
        self.reading_status = ReadingStatus.objects.create(
            user=self.user,
            book=self.book,
            status='reading'
        )

    def test_current_status(self):
        """
        Ensure user, book, and reading status is stored correctly
        """
        self.assertEqual(self.reading_status.user, self.user)
        self.assertEqual(self.reading_status.book, self.book)
        self.assertEqual(self.reading_status.status, 'reading')

    def test_change_status(self):
        """
        Ensure status change stores properly
        """
        self.reading_status.status = 'finished'

        self.assertEqual(self.reading_status.status, 'finished')

    def test_book_deletion_cascades(self):
        """
        Ensure book deletion removes reading status
        """
        self.assertEqual(ReadingStatus.objects.filter(book=self.book).count(), 1)
        self.book.delete()
        self.assertEqual(ReadingStatus.objects.filter(book=self.book).count(), 0)

    def test_user_deletion_cascades(self):
        """
        Ensure user deletion removes reading status
        """
        self.assertEqual(ReadingStatus.objects.filter(user=self.user).count(), 1)
        self.user.delete()
        self.assertEqual(ReadingStatus.objects.filter(user=self.user).count(), 0)

class ReadingProgressTest(TestCase):
    def setUp(self):
        """
        Create generic user and book
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            isbn='1234567890123'
        )

    def test_create_pages(self):
        """
        Ensure page tracking type stores properly
        """
        self.book.book_type = 'paper-book'
        self.book.length_pages = 200

        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='page',
            current_page=50
        )

        self.assertEqual(reading_progress.user, self.user)
        self.assertEqual(reading_progress.book, self.book)
        self.assertEqual(reading_progress.tracking_type, 'page')
        self.assertEqual(reading_progress.current_page, 50)

    def test_update_pages(self):
        """
        Ensure pages tracking type updates properly
        """
        self.book.book_type = 'paper-book'
        self.book.length_pages = 200

        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='page',
            current_page=50
        )

        reading_progress.current_page = 75
        reading_progress.save()

        updated_reading_progress = ReadingProgress.objects.get(id=reading_progress.id)
        self.assertEqual(updated_reading_progress.current_page, 75)

    def test_create_percentage(self):
        """
        Ensure percentage tracking type stores properly
        """
        self.book.book_type = 'e-book'
        
        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='percentage',
            current_percent=0
        )

        self.assertEqual(reading_progress.user, self.user)
        self.assertEqual(reading_progress.book, self.book)
        self.assertEqual(reading_progress.tracking_type, 'percentage')
        self.assertEqual(reading_progress.current_percent, 0)

    def test_update_percentage(self):
        """
        Ensure percentage tracking type updates properly
        """
        self.book.book_type = 'e-book'

        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='percentage'
        )

        reading_progress.current_percent = 15
        reading_progress.save()

        updated_reading_progress = ReadingProgress.objects.get(id=reading_progress.id)
        self.assertEqual(updated_reading_progress.current_percent, 15)

    def test_create_time(self):
        """
        Ensure time tracking type stores properly
        """
        self.book.book_type = 'audio-book'
        self.book.length_time = timedelta(
            hours=2,
            minutes=30,
        )

        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='time',
            current_time=timedelta(
                hours=0,
                minutes=0,
            )
        )

        self.assertEqual(reading_progress.user, self.user)
        self.assertEqual(reading_progress.book, self.book)
        self.assertEqual(reading_progress.tracking_type, 'time')
        self.assertEqual(reading_progress.current_time.total_seconds(), 0)

    def test_update_time(self):
        """
        Ensure time tracking type updates properly
        """
        self.book.book_type = 'audio-book'
        self.book.length_time = timedelta(
            hours=2,
            minutes=30,
        )

        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='time',
            current_time=timedelta(
                hours=0,
                minutes=0,
            )
        )

        reading_progress.current_time = timedelta(
            hours=1,
        )
        reading_progress.save()

        updated_reading_progress = ReadingProgress.objects.get(id=reading_progress.id)
        self.assertEqual(updated_reading_progress.current_time.total_seconds(), 3600)

    def test_book_deletion_cascades(self):
        """
        Ensure book deletion removes reading progress
        """
        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='percentage'
        )
        
        self.assertEqual(ReadingProgress.objects.filter(book=self.book).count(), 1)
        self.book.delete()
        self.assertEqual(ReadingProgress.objects.filter(book=self.book).count(), 0)

    def test_user_deletion_cascades(self):
        """
        Ensure user deletion removes reading progress
        """
        reading_progress = ReadingProgress.objects.create(
            user=self.user,
            book=self.book,
            tracking_type='percentage'
        )

        self.assertEqual(ReadingProgress.objects.filter(user=self.user).count(), 1)
        self.user.delete()
        self.assertEqual(ReadingProgress.objects.filter(user=self.user).count(), 0)