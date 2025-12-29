from datetime import datetime, timedelta
import os

FILE_NAME = "books.txt"
FINE_PER_DAY = 1000  # Tsh 1000 kwa siku


# =========================
# Book Class
# =========================
class Book:
    def __init__(self, title, author, is_borrowed=False, due_date=None):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.due_date = due_date

    def to_file(self):
        return f"{self.title},{self.author},{self.is_borrowed},{self.due_date}\n"

    @staticmethod
    def from_file(line):
        title, author, is_borrowed, due_date = line.strip().split(",")
        due_date = None if due_date == "None" else datetime.fromisoformat(due_date)
        return Book(title, author, is_borrowed == "True", due_date)


# =========================
# Member Class
# =========================
class Member:
    def __init__(self, name):
        self.name = name


# =========================
# Library Class
# =========================
class Library:
    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                for line in file:
                    self.books.append(Book.from_file(line))
        else:
            # Vitabu vya mwanzo
            self.books = [
                Book("Python Basics", "John Doe"),
                Book("Data Structures", "Jane Smith"),
                Book("AI for Beginners", "Alan Turing")
            ]
            self.save_books()

    def save_books(self):
        with open(FILE_NAME, "w") as file:
            for book in self.books:
                file.write(book.to_file())

    def show_books(self):
        print("\n📚 VITABU VILIVYOPO:")
        for book in self.books:
            status = "Available" if not book.is_borrowed else f"Borrowed (Due: {book.due_date.date()})"
            print(f"- {book.title} | {book.author} | {status}")

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.is_borrowed:
                book.is_borrowed = True
                book.due_date = datetime.now() + timedelta(days=7)
                self.save_books()
                print(f"\n✅ Kitabu kimekopwa. Rudisha kabla ya {book.due_date.date()}")
                return
        print("\n❌ Kitabu hakipo au tayari kimekopwa")

    def calculate_fine(self, book):
        if datetime.now() > book.due_date:
            late_days = (datetime.now() - book.due_date).days
            return late_days * FINE_PER_DAY
        return 0

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.is_borrowed:
                fine = self.calculate_fine(book)
                book.is_borrowed = False
                book.due_date = None
                self.save_books()
                if fine > 0:
                    print(f"\n⚠️ Umechelewa! Faini yako ni Tsh {fine}")
                else:
                    print("\n✅ Kitabu kimerudishwa kwa wakati")
                return
        print("\n❌ Kitabu hiki hakijakopwa")


# =========================
# MAIN MENU
# =========================
library = Library()
member_name = input("Ingiza jina lako: ")
member = Member(member_name)

while True:
    print("\n===== 📖 LIBRARY MENU =====")
    print("1. Onyesha vitabu")
    print("2. Kopa kitabu")
    print("3. Rudisha kitabu")
    print("4. Exit")

    choice = input("Chagua (1-4): ")

    if choice == "1":
        library.show_books()

    elif choice == "2":
        title = input("Ingiza jina la kitabu: ")
        library.borrow_book(title)

    elif choice == "3":
        title = input("Ingiza jina la kitabu: ")
        library.return_book(title)

    elif choice == "4":
        print("\n👋 Asante kwa kutumia Library Management System")
        break

    else:
        print("\n❌ Chaguo sio sahihi, jaribu tena")
