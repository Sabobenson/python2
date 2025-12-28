# python2
Python projects and practice codes


## 1️⃣ Msingi wa OOP

OOP inategemea **objects** na **classes**:

* **Class** – blueprint au template ya kitu. Inasema kitu kitakuwa na **properties (attributes)** na **behaviors (methods)**.
* **Object** – instance ya class. Kila object inapata copy yake ya attributes na methods.

**Mfano wa class na object:**

```python
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start_engine(self):
        print(f"{self.brand} {self.model} engine started.")

car1 = Car("Toyota", "Corolla", 2020)
car2 = Car("Honda", "Civic", 2019)

car1.start_engine()
car2.start_engine()
```

---

## 2️⃣ Four Pillars za OOP

### a) Encapsulation

Huficha details za implementation ndani ya class.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
print(account.get_balance())  # 1500
```

### b) Inheritance

Class inaweza kurithi attributes na methods kutoka kwa class nyingine.

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} vehicle started.")

class Motorcycle(Vehicle):
    def do_wheelie(self):
        print(f"{self.brand} is doing a wheelie!")

bike = Motorcycle("Yamaha")
bike.start()
bike.do_wheelie()
```

### c) Polymorphism

Method moja inaweza kufanya kazi tofauti kulingana na object.

```python
class Dog:
    def sound(self):
        print("Woof!")

class Cat:
    def sound(self):
        print("Meow!")

animals = [Dog(), Cat()]
for animal in animals:
    animal.sound()
```

### d) Abstraction

Kufanya class yenye interface rahisi, ikificha details ngumu.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

c = Circle(5)
print(c.area())  # 78.5
```

---

## 3️⃣ Faida za OOP kwa Projects Kubwa

1. **Code Organization** – kila kitu kiko kwenye classes, rahisi kufuatilia.
2. **Reuse & Maintainability** – methods na classes zinaweza kutumika tena.
3. **Flexibility & Extensibility** – unaweza kuongeza features mpya bila kuharibu existing code.
4. **Modeling Real-world Objects** – Rahisi kuelewa na ku-design system inayoendana na dunia halisi.

---

## 4️⃣ Mini Project Idea: Library Management System

* **Classes**: `Book`, `Member`, `Library`
* **Methods**: `borrow_book()`, `return_book()`, `show_books()`
* **Attributes**: `title`, `author`, `member_name`, `due_date`

Hii itakupa experience ya OOP fully.

---

**Tip:** Jaribu ku-design system yako, tengeneza objects, tests, na methods mbalimbali ili ufahamu fully pillars zote za OOP.
