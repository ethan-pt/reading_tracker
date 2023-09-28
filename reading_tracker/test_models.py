from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, ReadingStatus, ReadingProgress

from datetime import timedelta



class BookModelTest(TestCase):
    def test_create_paper_book(self):
        book = Book.objects.create(
            title="Test Paper Book",
            author="Test Author",
            publisher="Test Publisher",
            isbn="1234567890123",
            book_type="paper-book",
            length_pages=200,
        )

        self.assertEqual(book.title, 'Test Paper Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'paper-book')
        self.assertEqual(book.length_pages, 200)
        self.assertIsNone(book.length_time)

    def test_create_ebook(self):
        book = Book.objects.create(
            title="Test e-book",
            author="Test Author",
            publisher="Test Publisher",
            isbn="1234567890123",
            book_type="e-book",
        )

        self.assertEqual(book.title, 'Test e-book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'e-book')
        self.assertIsNone(book.length_pages)
        self.assertIsNone(book.length_time)

    def test_create_audio_book(self):
        book = Book.objects.create(
            title="Test Audio Book",
            author="Test Author",
            publisher="Test Publisher",
            isbn="1234567890123",
            book_type="audio-book",
            length_time=timedelta(
                hours=2,
                minutes=30
            ),
        )

        self.assertEqual(book.title, 'Test Audio Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publisher, 'Test Publisher')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.book_type, 'audio-book')
        self.assertEqual(book.length_time.total_seconds(), 9000)
        self.assertIsNone(book.length_pages)