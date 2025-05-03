import json
import os

BOOK_FILE = "books.json"

def load_books():
    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "r") as f:
            return json.load(f)
    return []

def save_books(books):
    with open(BOOK_FILE, "w") as f:
        json.dump(books, f, indent=2)

def add_book(title, author):
    books = load_books()
    books.append({"title": title, "author": author, "status": "unread"})
    save_books(books)
    print(f"📚 Added: {title} by {author}")

def list_books():
    books = load_books()
    if not books:
        print("No books found.")
        return
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['title']} by {book['author']} - {book['status']}")

def mark_as_read(index):
    books = load_books()
    if 0 <= index < len(books):
        books[index]["status"] = "read"
        save_books(books)
        print(f"✅ Marked '{books[index]['title']}' as read.")
    else:
        print("Invalid book index.")

def main():
    while True:
        print("\nBook Tracker Menu:")
        print("1. Add a book")
        print("2. List all books")
        print("3. Mark a book as read")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            add_book(title, author)
        elif choice == "2":
            list_books()
        elif choice == "3":
            list_books()
            index = int(input("Enter the book number to mark as read: ")) - 1
            mark_as_read(index)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

