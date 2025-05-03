import json
import os

BOOK_FILE = "books.json"

def load_books():
    """Loads the book list from the JSON file."""
    if os.path.exists(BOOK_FILE):
        try:
            with open(BOOK_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {BOOK_FILE}. Starting with an empty list.")
            return []
    return []

def save_books(books):
    """Saves the book list to the JSON file."""
    with open(BOOK_FILE, "w") as f:
        json.dump(books, f, indent=2)

def add_book(title, author):
    """Adds a new book to the list."""
    books = load_books()
    books.append({"title": title, "author": author, "status": "unread"})
    save_books(books)
    print(f" Added: '{title}' by {author}")

def list_books():
    """Lists all books with their index and status."""
    books = load_books()
    if not books:
        print("No books found.")
        return False # Indicate that no books were found
    print("\n--- Your Books ---")
    for idx, book in enumerate(books): # Start index from 0 for internal logic
        print(f"{idx + 1}. {book['title']} by {book['author']} - {book['status']}")
    print("------------------")
    return True # Indicate that books were listed

def mark_as_read(index):
    """Marks a book as 'read' based on its 0-based index."""
    books = load_books()
    if 0 <= index < len(books):
        if books[index]["status"] == "read":
             print(f"'{books[index]['title']}' is already marked as read.")
        else:
            books[index]["status"] = "read"
            save_books(books)
            print(f" Marked '{books[index]['title']}' as read.")
    else:
        print("Invalid book number.")

def delete_book(index):
    """Deletes a book from the list based on its 0-based index."""
    books = load_books()
    if 0 <= index < len(books):
        deleted_book = books.pop(index) # pop removes and returns the item
        save_books(books)
        print(f" Deleted '{deleted_book['title']}'.")
    else:
        print("Invalid book number.") # Consistent error message

def get_valid_index(prompt):
    """Gets and validates user input for a book index."""
    while True:
        try:
            choice = input(prompt).strip()
            if not choice: # Handle empty input
                print("Input cannot be empty.")
                continue
            index = int(choice) - 1 # Convert to 0-based index
            return index
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Main function to run the Book Tracker application."""
    while True:
        print("\n--- Book Tracker Menu ---")
        print("1. Add a new book")
        print("2. List all books")
        print("3. Mark a book as read")
        print("4. Delete a book")
        print("5. Exit")
        print("-------------------------")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            if title and author: # Basic validation
                 add_book(title, author)
            else:
                 print("Title and Author cannot be empty.")
        elif choice == "2":
            list_books()
        elif choice == "3":
            if list_books(): # Only ask for index if books exist
                index = get_valid_index("Enter the book number to mark as read: ")
                mark_as_read(index)
        elif choice == "4":
             if list_books(): # Only ask for index if books exist
                index = get_valid_index("Enter the book number to delete: ")
                delete_book(index)
        elif choice == "5":
            print("Exiting Book Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    # Ensure the JSON file exists or create it
    if not os.path.exists(BOOK_FILE):
        save_books([]) # Create an empty file if it doesn't exist
    main()
