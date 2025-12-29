# =========================
# Book Class
# =========================
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False


# =========================
# Member Class
# =========================
class Member:
    def __init__(self, member_name):
        self.member_name = member_name
        self.borrowed_books = []


# =========================
# Library Class
# =========================
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def show_books(self):
        print("\n📚 LIST YA VITABU:")
        if not self.books:
            print("Hakuna vitabu kwenye maktaba.")
        for book in self.books:
            status = "Available" if not book.is_borrowed else "Borrowed"
            print(f"- {book.title} | {book.author} | {status}")

    def borrow_book(self, title, member):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.is_borrowed:
                book.is_borrowed = True
                member.borrowed_books.append(book)
                print(f"\n✅ {member.member_name} amekopa '{book.title}'")
                return
        print("\n❌ Kitabu hakipo au tayari kimekopwa")

    def return_book(self, title, member):
        for book in member.borrowed_books:
            if book.title.lower() == title.lower():
                book.is_borrowed = False
                member.borrowed_books.remove(book)
                print(f"\n🔁 {member.member_name} amerudisha '{book.title}'")
                return
        print("\n❌ Kitabu hiki hakikukopwa na member huyu")


# =========================
# MAIN PROGRAM (MENU)
# =========================
library = Library()

# Add sample books
library.add_book(Book("Python Basics", "John Doe"))
library.add_book(Book("Data Structures", "Jane Smith"))
library.add_book(Book("AI for Beginners", "Alan Turing"))

# Create member
name = input("Ingiza jina la member: ")
member = Member(name)

while True:
    print("\n===== LIBRARY MENU =====")
    print("1. Onyesha vitabu")
    print("2. Kopa kitabu")
    print("3. Rudisha kitabu")
    print("4. Exit")

    choice = input("Chagua (1-4): ")

    if choice == "1":
        library.show_books()

    elif choice == "2":
        title = input("Ingiza jina la kitabu: ")
        library.borrow_book(title, member)

    elif choice == "3":
        title = input("Ingiza jina la kitabu: ")
        library.return_book(title, member)

    elif choice == "4":
        print("\n👋 Asante kwa kutumia Library System")
        break

    else:
        print("\n❌ Chaguo sio sahihi, jaribu tena")

# =========================
# END OF PROGRAM

