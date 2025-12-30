from datetime import datetime, timedelta
import os
import hashlib

# ================= CONFIG =================
MAX_BOOKS_PER_MEMBER = 2
FINE_PER_DAY = 1000
BOOKS_FILE = "books.txt"
MEMBERS_FILE = "members.txt"

MAX_LOGIN_ATTEMPTS = 3
LOCK_MINUTES = 5

# ================= SECURITY =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= BOOK =================
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

# ================= MEMBER =================
class Member:
    def __init__(self, username, password, role="member",
                 books=None, failed_attempts=0, lock_until=None):
        self.username = username
        self.password = password
        self.role = role
        self.books = books or []
        self.failed_attempts = failed_attempts
        self.lock_until = lock_until

    def is_admin(self):
        return self.role == "admin"

    def is_locked(self):
        if self.lock_until and datetime.now() < self.lock_until:
            return True
        return False

    def lock_remaining_minutes(self):
        if self.lock_until:
            delta = self.lock_until - datetime.now()
            return max(0, int(delta.total_seconds() // 60) + 1)
        return 0

    def to_file(self):
        return (
            f"{self.username}|{self.password}|{self.role}|"
            f"{','.join(self.books)}|{self.failed_attempts}|{self.lock_until}\n"
        )

    @classmethod
    def from_file(cls, line):
        parts = line.strip().split("|")
        if len(parts) < 6:
            return None

        books = parts[3].split(",") if parts[3] else []
        failed = int(parts[4])
        lock = None if parts[5] == "None" else datetime.fromisoformat(parts[5])

        return cls(parts[0], parts[1], parts[2], books, failed, lock)

# ================= LIBRARY =================
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.setup_files()
        self.load_books()
        self.load_members()

    # ---------- FILE SETUP ----------
    def setup_files(self):
        if not os.path.exists(MEMBERS_FILE):
            with open(MEMBERS_FILE, "w") as f:
                f.write(
                    f"admin|{hash_password('admin123')}|admin||0|None\n"
                )

        if not os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, "w") as f:
                f.write("AI for Beginners|John Doe|False|None|None\n")

    def load_books(self):
        with open(BOOKS_FILE) as f:
            for line in f:
                book = Book.from_file(line)
                if book:
                    self.books.append(book)

    def load_members(self):
        with open(MEMBERS_FILE) as f:
            for line in f:
                member = Member.from_file(line)
                if member:
                    self.members.append(member)

    def save_members(self):
        with open(MEMBERS_FILE, "w") as f:
            for m in self.members:
                f.write(m.to_file())

    def save_books(self):
        with open(BOOKS_FILE, "w") as f:
            for b in self.books:
                f.write(b.to_file())

    def find_member(self, username):
        for m in self.members:
            if m.username == username:
                return m
        return None

    # ---------- AUTH ----------
    def login(self):
        u = input("Username: ")
        m = self.find_member(u)

        if not m:
            print("❌ User not found")
            return None

        if m.is_locked():
            print(
                f"🔒 Account locked. Try again in "
                f"{m.lock_remaining_minutes()} minute(s)"
            )
            return None

        p = hash_password(input("Password: "))

        if p == m.password:
            m.failed_attempts = 0
            m.lock_until = None
            self.save_members()
            print(f"✅ Login successful ({m.role})")
            return m

        # WRONG PASSWORD
        m.failed_attempts += 1
        if m.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            m.lock_until = datetime.now() + timedelta(minutes=LOCK_MINUTES)
            print(f"🔒 Account locked for {LOCK_MINUTES} minutes")
        else:
            print(
                f"❌ Wrong password "
                f"({m.failed_attempts}/{MAX_LOGIN_ATTEMPTS})"
            )

        self.save_members()
        return None

    def register(self):
        u = input("New username: ")
        if self.find_member(u):
            print("❌ Username exists")
            return None
        p = hash_password(input("Password: "))
        m = Member(u, p)
        self.members.append(m)
        self.save_members()
        print("✅ Registered successfully")
        return m

    def change_password(self, member):
        old = hash_password(input("Old password: "))
        if old != member.password:
            print("❌ Wrong old password")
            return
        new = hash_password(input("New password: "))
        member.password = new
        self.save_members()
        print("✅ Password changed")

    # ---------- OPERATIONS ----------
    def show_books(self):
        print("\n📚 BOOKS")
        for b in self.books:
            status = "Available" if not b.is_borrowed else f"Borrowed by {b.borrowed_by}"
            print(f"{b.title} - {b.author} [{status}]")

    def add_book(self):
        title = input("Book title: ")
        author = input("Author: ")
        self.books.append(Book(title, author))
        self.save_books()
        print("✅ Book added")

    def borrow_book(self, member):
        if len(member.books) >= MAX_BOOKS_PER_MEMBER:
            print("❌ Maximum books reached")
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
        print("❌ Book not available")

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

# ================= MAIN =================
def main():
    library = Library()

    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        c = input("Choose: ")

        if c == "1":
            user = library.login()
        elif c == "2":
            user = library.register()
        else:
            break

        while user:
            if user.is_admin():
                print("\nADMIN MENU")
                print("1. Add Book")
                print("2. Show Books")
                print("3. Change Password")
                print("4. Logout")
                ch = input("Choose: ")
                if ch == "1":
                    library.add_book()
                elif ch == "2":
                    library.show_books()
                elif ch == "3":
                    library.change_password(user)
                elif ch == "4":
                    break
            else:
                print("\nMEMBER MENU")
                print("1. Show Books")
                print("2. Borrow")
                print("3. Return")
                print("4. Change Password")
                print("5. Logout")
                ch = input("Choose: ")
                if ch == "1":
                    library.show_books()
                elif ch == "2":
                    library.borrow_book(user)
                elif ch == "3":
                    library.return_book(user)
                elif ch == "4":
                    library.change_password(user)
                elif ch == "5":
                    break

main()
