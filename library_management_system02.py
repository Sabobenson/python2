from datetime import datetime, timedelta
import os

MAX_BOOKS_PER_MEMBER = 2
FINE_PER_DAY = 1000

# ---------------- BOOK ----------------
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.due_date = None
        self.borrowed_by = None

    def borrow(self, member):
        self.is_borrowed = True
        self.borrowed_by = member.username
        self.due_date = datetime.now() + timedelta(days=7)

    def return_book(self):
        self.is_borrowed = False
        self.borrowed_by = None
        self.due_date = None

    def fine(self):
        if self.due_date and datetime.now() > self.due_date:
            return (datetime.now() - self.due_date).days * FINE_PER_DAY
        return 0

    def to_file(self):
        return f"{self.title}|{self.author}|{self.is_borrowed}|{self.due_date}|{self.borrowed_by}\n"

    @classmethod
    def from_file(cls, line):
        parts = line.strip().split("|")
        if len(parts) != 5:
            return None
        title, author, borrowed, due, by = parts
        book = cls(title, author)
        book.is_borrowed = borrowed == "True"
        book.due_date = None if due == "None" else datetime.fromisoformat(due)
        book.borrowed_by = None if by == "None" else by
        return book


# ---------------- MEMBER ----------------
class Member:
    def __init__(self, username, password, books=None):
        self.username = username
        self.password = password
        self.books = books or []

    def can_borrow(self):
        return len(self.books) < MAX_BOOKS_PER_MEMBER

    def to_file(self):
        return f"{self.username}|{self.password}|{','.join(self.books)}\n"

    @classmethod
    def from_file(cls, line):
        parts = line.strip().split("|")
        if len(parts) < 2:
            return None
        books = parts[2].split(",") if len(parts) == 3 and parts[2] else []
        return cls(parts[0], parts[1], books)


# ---------------- LIBRARY ----------------
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.load_books()
        self.load_members()

    def load_books(self):
        if not os.path.exists("books.txt"):
            return
        with open("books.txt") as f:
            for line in f:
                book = Book.from_file(line)
                if book:
                    self.books.append(book)

    def save_books(self):
        with open("books.txt", "w") as f:
            for b in self.books:
                f.write(b.to_file())

    def load_members(self):
        if not os.path.exists("members.txt"):
            return
        with open("members.txt") as f:
            for line in f:
                m = Member.from_file(line)
                if m:
                    self.members.append(m)

    def save_members(self):
        with open("members.txt", "w") as f:
            for m in self.members:
                f.write(m.to_file())

    def find_member(self, username):
        return next((m for m in self.members if m.username == username), None)

    def login(self):
        u = input("Username: ")
        p = input("Password: ")
        m = self.find_member(u)
        if m and m.password == p:
            print("✅ Login successful")
            return m
        print("❌ Invalid login")
        return None

    def register(self):
        u = input("New username: ")
        if self.find_member(u):
            print("❌ Username exists")
            return None
        p = input("Password: ")
        m = Member(u, p)
        self.members.append(m)
        self.save_members()
        print("✅ Registered successfully")
        return m

    def show_books(self):
        for b in self.books:
            status = "Available" if not b.is_borrowed else f"Borrowed by {b.borrowed_by}"
            print(f"{b.title} - {b.author} [{status}]")

    def borrow_book(self, member):
        if not member.can_borrow():
            print("❌ Max books reached")
            return
        title = input("Book title: ")
        for b in self.books:
            if b.title.lower() == title.lower() and not b.is_borrowed:
                b.borrow(member)
                member.books.append(b.title)
                self.save_books()
                self.save_members()
                print("✅ Book borrowed")
                return
        print("❌ Book unavailable")

    def return_book(self, member):
        title = input("Book title: ")
        for b in self.books:
            if b.title.lower() == title.lower() and b.borrowed_by == member.username:
                fine = b.fine()
                b.return_book()
                member.books.remove(b.title)
                self.save_books()
                self.save_members()
                print(f"✅ Returned | Fine: {fine} TZS")
                return
        print("❌ Book not found")


# ---------------- MAIN ----------------
def main():
    lib = Library()

    if not lib.books:
        lib.books.append(Book("AI for Beginners", "John Doe"))
        lib.books.append(Book("Python Basics", "Jane Smith"))
        lib.save_books()

    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        c = input("Choose: ")

        if c == "1":
            member = lib.login()
        elif c == "2":
            member = lib.register()
        else:
            break

        while member:
            print("\n1.Show Books\n2.Borrow\n3.Return\n4.Logout")
            ch = input("Choose: ")
            if ch == "1":
                lib.show_books()
            elif ch == "2":
                lib.borrow_book(member)
            elif ch == "3":
                lib.return_book(member)
            elif ch == "4":
                break

main()
