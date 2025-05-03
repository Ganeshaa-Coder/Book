import unittest
import os
import json
import io  # Added import io
from Book_Tracker import load_books, save_books, add_book, mark_as_read, list_books
from unittest.mock import patch, MagicMock

class TestBookTracker(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_book_file = "test_books.json"
        # Start patcher for Book_Tracker.BOOK_FILE
        self.mock_book_file = patch('Book_Tracker.BOOK_FILE', self.test_book_file)
        self.mock_book_file.start() # Start the patcher

        # Ensure the test file is clean before each test
        if os.path.exists(self.test_book_file):
            os.remove(self.test_book_file)

    def tearDown(self):
        """Tear down test environment."""
        # Stop the patcher
        self.mock_book_file.stop()

        # Clean up the test file after each test
        if os.path.exists(self.test_book_file):
            os.remove(self.test_book_file)

    def test_load_books_no_file(self):
        """Test loading books when the file does not exist."""
        self.assertEqual(load_books(), [])

    def test_load_books_empty_file(self):
        """Test loading books from an empty file."""
        save_books([])
        self.assertEqual(load_books(), [])

    def test_load_books_with_data(self):
        """Test loading books from a file with data."""
        sample_data = [{"title": "Test Book", "author": "Test Author", "status": "unread"}]
        save_books(sample_data)
        self.assertEqual(load_books(), sample_data)

    def test_save_books_empty_list(self):
        """Test saving an empty list of books."""
        save_books([])
        with open(self.test_book_file, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, [])

    def test_save_books_with_data(self):
        """Test saving a list of books with data."""
        sample_data = [{"title": "Save Test", "author": "Tester", "status": "read"}]
        save_books(sample_data)
        with open(self.test_book_file, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, sample_data)

    def test_add_book_first(self):
        """Test adding the first book."""
        add_book("First Title", "First Author")
        loaded_data = load_books()
        self.assertEqual(loaded_data, [{"title": "First Title", "author": "First Author", "status": "unread"}])

    def test_add_book_subsequent(self):
        """Test adding a book when data already exists."""
        initial_data = [{"title": "Initial Book", "author": "Initial Author", "status": "read"}]
        save_books(initial_data)
        add_book("Second Title", "Second Author")
        loaded_data = load_books()
        expected_data = initial_data + [{"title": "Second Title", "author": "Second Author", "status": "unread"}]
        self.assertEqual(loaded_data, expected_data)

    def test_mark_as_read_valid_index(self):
        """Test marking a book as read with a valid index."""
        initial_data = [{"title": "Test", "author": "Tester", "status": "unread"}]
        save_books(initial_data)
        mark_as_read(0)
        loaded_data = load_books()
        self.assertEqual(loaded_data[0]["status"], "read")

    def test_mark_as_read_invalid_index_positive(self):
        """Test marking a book as read with an invalid positive index."""
        initial_data = [{"title": "Test", "author": "Tester", "status": "unread"}]
        save_books(initial_data)
        mark_as_read(1) # Index out of bounds
        loaded_data = load_books()
        self.assertEqual(loaded_data, initial_data) # Data should be unchanged

    def test_mark_as_read_invalid_index_negative(self):
        """Test marking a book as read with a negative index."""
        initial_data = [{"title": "Test", "author": "Tester", "status": "unread"}]
        save_books(initial_data)
        mark_as_read(-1) # Negative index
        loaded_data = load_books()
        self.assertEqual(loaded_data, initial_data) # Data should be unchanged

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_books_empty(self, mock_stdout):
        """Test listing books when the list is empty."""
        list_books()
        self.assertEqual(mock_stdout.getvalue(), "No books found.\n")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_list_books_with_data(self, mock_stdout):
        """Test listing books when there is data."""
        sample_data = [{"title": "List Test 1", "author": "Author A", "status": "unread"}, {"title": "List Test 2", "author": "Author B", "status": "read"}]
        save_books(sample_data)
        list_books()
        expected_output = "1. List Test 1 by Author A - unread\n2. List Test 2 by Author B - read\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
