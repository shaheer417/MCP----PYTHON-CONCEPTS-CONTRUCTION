"""
OBJECT-ORIENTED PROGRAMMING (OOP) - BEGINNER LEVEL
===================================================

Essential OOP concepts for MCP understanding - Part 1

Topics Covered:
1. Classes and Objects (Basic)
2. Attributes (Instance and Class)
3. Methods (Instance, Class, Static)
4. The __init__ Constructor
5. The self Parameter
6. Encapsulation Basics
7. Simple Property Decorators

These are building blocks for understanding MCP architecture!
"""

# ============================================================================
# EXAMPLE 1: Basic Class and Object Creation
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 1: Basic Class and Object")
print("="*70)

class Dog:
    """A simple Dog class"""
    pass

# Creating objects (instances)
dog1 = Dog()
dog2 = Dog()

print(f"dog1 is a: {type(dog1)}")
print(f"dog2 is a: {type(dog2)}")
print(f"Are they the same object? {dog1 is dog2}")  # False - different instances


# ============================================================================
# EXAMPLE 2: Class with Attributes
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 2: Class Attributes and Instance Attributes")
print("="*70)

class Cat:
    # Class attribute (shared by all instances)
    species = "Felis catus"

    def __init__(self, name, age):
        # Instance attributes (unique to each instance)
        self.name = name
        self.age = age

cat1 = Cat("Whiskers", 3)
cat2 = Cat("Shadow", 5)

print(f"Cat 1: {cat1.name}, Age: {cat1.age}, Species: {cat1.species}")
print(f"Cat 2: {cat2.name}, Age: {cat2.age}, Species: {cat2.species}")

# Class attribute is shared
print(f"\nChanging species for all cats...")
Cat.species = "Domestic Cat"
print(f"Cat 1 species: {cat1.species}")
print(f"Cat 2 species: {cat2.species}")


# ============================================================================
# EXAMPLE 3: Instance Methods
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 3: Instance Methods")
print("="*70)

class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.odometer = 0

    def get_description(self):
        """Return formatted description"""
        return f"{self.year} {self.brand} {self.model}"

    def drive(self, miles):
        """Simulate driving"""
        self.odometer += miles
        return f"Drove {miles} miles. Total: {self.odometer} miles"

    def read_odometer(self):
        """Display odometer reading"""
        return f"This car has {self.odometer} miles on it."

my_car = Car("Toyota", "Camry", 2020)
print(my_car.get_description())
print(my_car.drive(100))
print(my_car.drive(50))
print(my_car.read_odometer())


# ============================================================================
# EXAMPLE 4: The __init__ Constructor in Detail
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 4: Understanding __init__ Constructor")
print("="*70)

class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        """Initialize bank account with holder name and optional balance"""
        self.account_holder = account_holder
        self.balance = initial_balance
        print(f"Account created for {account_holder} with balance ${initial_balance}")

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited ${amount}. New balance: ${self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        return f"Withdrew ${amount}. New balance: ${self.balance}"

# Creating accounts
account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob")  # Uses default balance

print(account1.deposit(500))
print(account1.withdraw(200))
print(account2.deposit(100))


# ============================================================================
# EXAMPLE 5: Understanding 'self'
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 5: Understanding the 'self' Parameter")
print("="*70)

class Person:
    def __init__(self, name, age):
        self.name = name  # self refers to the instance being created
        self.age = age

    def introduce(self):
        # self allows accessing instance attributes
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

    def have_birthday(self):
        # self allows modifying instance attributes
        self.age += 1
        return f"Happy birthday {self.name}! You're now {self.age}."

person1 = Person("John", 25)
person2 = Person("Jane", 30)

print(person1.introduce())
print(person2.introduce())
print(person1.have_birthday())
print(person1.introduce())


# ============================================================================
# EXAMPLE 6: Class Methods vs Instance Methods
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 6: Class Methods with @classmethod")
print("="*70)

class Pizza:
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings

    def describe(self):
        """Instance method"""
        return f"{self.size} pizza with {', '.join(self.toppings)}"

    @classmethod
    def margherita(cls, size):
        """Class method - alternative constructor"""
        return cls(size, ['mozzarella', 'tomato', 'basil'])

    @classmethod
    def pepperoni(cls, size):
        """Class method - alternative constructor"""
        return cls(size, ['mozzarella', 'pepperoni'])

# Using regular constructor
pizza1 = Pizza("Large", ["mushrooms", "olives"])
print(pizza1.describe())

# Using class methods as factory methods
pizza2 = Pizza.margherita("Medium")
pizza3 = Pizza.pepperoni("Large")

print(pizza2.describe())
print(pizza3.describe())


# ============================================================================
# EXAMPLE 7: Static Methods
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 7: Static Methods with @staticmethod")
print("="*70)

class MathOperations:
    """Utility class for math operations"""

    @staticmethod
    def add(x, y):
        """Static method - doesn't need instance or class"""
        return x + y

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def is_even(num):
        return num % 2 == 0

# Can call without creating instance
print(f"5 + 3 = {MathOperations.add(5, 3)}")
print(f"5 * 3 = {MathOperations.multiply(5, 3)}")
print(f"Is 4 even? {MathOperations.is_even(4)}")
print(f"Is 7 even? {MathOperations.is_even(7)}")


# ============================================================================
# EXAMPLE 8: Encapsulation - Public vs Private Attributes
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 8: Encapsulation Basics")
print("="*70)

class Employee:
    def __init__(self, name, salary):
        self.name = name              # Public attribute
        self._department = "General"  # Protected attribute (convention)
        self.__salary = salary        # Private attribute (name mangling)

    def get_salary(self):
        """Public method to access private attribute"""
        return self.__salary

    def set_salary(self, new_salary):
        """Public method to modify private attribute with validation"""
        if new_salary > 0:
            self.__salary = new_salary
            return f"Salary updated to ${new_salary}"
        return "Invalid salary amount"

    def get_info(self):
        return f"{self.name} earns ${self.__salary}"

emp = Employee("Alice", 50000)

print(f"Name (public): {emp.name}")
print(f"Department (protected): {emp._department}")
# print(emp.__salary)  # This would raise AttributeError
print(f"Salary (via method): {emp.get_salary()}")
print(emp.set_salary(55000))
print(emp.get_info())


# ============================================================================
# EXAMPLE 9: Property Decorators (@property)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 9: Property Decorators")
print("="*70)

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """Get temperature in Celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius with validation"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit"""
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature using Fahrenheit"""
        self._celsius = (value - 32) * 5/9

temp = Temperature(25)
print(f"Temperature: {temp.celsius}°C = {temp.fahrenheit}°F")

# Using property setter
temp.celsius = 30
print(f"After update: {temp.celsius}°C = {temp.fahrenheit}°F")

# Setting via Fahrenheit
temp.fahrenheit = 68
print(f"Set to 68°F: {temp.celsius}°C = {temp.fahrenheit}°F")


# ============================================================================
# EXAMPLE 10: String Representation Methods (__str__ and __repr__)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 10: String Representation Methods")
print("="*70)

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """User-friendly string representation"""
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        """Developer-friendly representation"""
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

book = Book("1984", "George Orwell", 328)

print(f"str(book): {str(book)}")      # Calls __str__
print(f"repr(book): {repr(book)}")    # Calls __repr__
print(f"Just book: {book}")           # Defaults to __str__


# ============================================================================
# EXAMPLE 11: Class Variables vs Instance Variables
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 11: Class vs Instance Variables")
print("="*70)

class Student:
    # Class variable - shared across all instances
    school_name = "Python Academy"
    total_students = 0

    def __init__(self, name, grade):
        # Instance variables - unique to each instance
        self.name = name
        self.grade = grade
        Student.total_students += 1  # Increment class variable

    def display_info(self):
        return f"{self.name}, Grade: {self.grade}, School: {Student.school_name}"

student1 = Student("Alice", "A")
student2 = Student("Bob", "B")
student3 = Student("Charlie", "A")

print(student1.display_info())
print(student2.display_info())
print(f"Total students: {Student.total_students}")


# ============================================================================
# EXAMPLE 12: Method Chaining
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 12: Method Chaining")
print("="*70)

class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, num):
        self.value += num
        return self  # Return self for chaining

    def subtract(self, num):
        self.value -= num
        return self

    def multiply(self, num):
        self.value *= num
        return self

    def divide(self, num):
        if num != 0:
            self.value /= num
        return self

    def result(self):
        return self.value

# Method chaining in action
calc = Calculator()
result = calc.add(10).multiply(5).subtract(20).divide(2).result()
print(f"Result of chained operations: {result}")


# ============================================================================
# EXAMPLE 13: Object Comparison Methods
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 13: Object Comparison")
print("="*70)

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        """Equal comparison"""
        return self.price == other.price

    def __lt__(self, other):
        """Less than comparison"""
        return self.price < other.price

    def __str__(self):
        return f"{self.name}: ${self.price}"

product1 = Product("Laptop", 1000)
product2 = Product("Phone", 500)
product3 = Product("Tablet", 500)

print(f"{product1} == {product2}: {product1 == product2}")
print(f"{product2} == {product3}: {product2 == product3}")
print(f"{product2} < {product1}: {product2 < product1}")
print(f"{product1} < {product2}: {product1 < product2}")


# ============================================================================
# EXAMPLE 14: Container Methods (Making classes iterable)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 14: Making Classes Iterable")
print("="*70)

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __len__(self):
        """Support len() function"""
        return len(self.songs)

    def __getitem__(self, index):
        """Support indexing and iteration"""
        return self.songs[index]

    def __contains__(self, song):
        """Support 'in' operator"""
        return song in self.songs

playlist = Playlist("My Favorites")
playlist.add_song("Song A")
playlist.add_song("Song B")
playlist.add_song("Song C")

print(f"Playlist length: {len(playlist)}")
print(f"First song: {playlist[0]}")
print(f"Is 'Song B' in playlist? {'Song B' in playlist}")
print(f"Is 'Song Z' in playlist? {'Song Z' in playlist}")

print("\nIterating through playlist:")
for song in playlist:
    print(f"  - {song}")


# ============================================================================
# EXAMPLE 15: Context Managers (__enter__ and __exit__)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 15: Context Managers (with statement)")
print("="*70)

class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        if self.file:
            print(f"Closing file: {self.filename}")
            self.file.close()
        return False

# Using context manager
with FileManager("test.txt") as f:
    f.write("Hello, World!\n")
    f.write("Context managers are cool!")

print("File operations completed!")


# ============================================================================
# EXAMPLE 16: Callable Objects (__call__)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 16: Callable Objects")
print("="*70)

class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        """Makes instance callable like a function"""
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")
print(f"double(10) = {double(10)}")


# ============================================================================
# EXAMPLE 17: Getter and Setter Methods (Traditional Approach)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 17: Traditional Getters and Setters")
print("="*70)

class Rectangle:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_width(self):
        return self.__width

    def set_width(self, width):
        if width > 0:
            self.__width = width
        else:
            raise ValueError("Width must be positive")

    def get_height(self):
        return self.__height

    def set_height(self, height):
        if height > 0:
            self.__height = height
        else:
            raise ValueError("Height must be positive")

    def area(self):
        return self.__width * self.__height

rect = Rectangle(10, 5)
print(f"Width: {rect.get_width()}, Height: {rect.get_height()}")
print(f"Area: {rect.area()}")

rect.set_width(15)
print(f"New width: {rect.get_width()}")
print(f"New area: {rect.area()}")


# ============================================================================
# EXAMPLE 18: Class Documentation and Attributes
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 18: Class Documentation")
print("="*70)

class Animal:
    """
    A class representing an animal.

    Attributes:
        name (str): The name of the animal
        species (str): The species of the animal
        age (int): The age of the animal in years
    """

    def __init__(self, name, species, age):
        """
        Initialize an Animal instance.

        Args:
            name (str): The name of the animal
            species (str): The species of the animal
            age (int): The age in years
        """
        self.name = name
        self.species = species
        self.age = age

    def make_sound(self):
        """
        Make the animal produce a sound.

        Returns:
            str: A string representing the sound
        """
        return f"{self.name} makes a sound"

animal = Animal("Leo", "Lion", 5)
print(f"Class docstring: {Animal.__doc__}")
print(f"Method docstring: {Animal.make_sound.__doc__}")
print(f"Instance: {animal.make_sound()}")


# ============================================================================
# EXAMPLE 19: Object Attribute Management
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 19: Dynamic Attribute Management")
print("="*70)

class DynamicObject:
    def __init__(self, name):
        self.name = name

    def add_attribute(self, attr_name, attr_value):
        """Dynamically add attribute"""
        setattr(self, attr_name, attr_value)

    def get_attribute(self, attr_name, default=None):
        """Safely get attribute"""
        return getattr(self, attr_name, default)

    def has_attribute(self, attr_name):
        """Check if attribute exists"""
        return hasattr(self, attr_name)

    def remove_attribute(self, attr_name):
        """Remove attribute"""
        if hasattr(self, attr_name):
            delattr(self, attr_name)

obj = DynamicObject("MyObject")
print(f"Initial name: {obj.name}")

obj.add_attribute("color", "blue")
obj.add_attribute("size", 10)

print(f"Color: {obj.get_attribute('color')}")
print(f"Size: {obj.get_attribute('size')}")
print(f"Has 'color'? {obj.has_attribute('color')}")

obj.remove_attribute("size")
print(f"After removing 'size': {obj.get_attribute('size', 'Not found')}")


# ============================================================================
# EXAMPLE 20: Simple Design Pattern - Singleton (Beginner-Friendly)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 20: Simple Singleton Pattern")
print("="*70)

class DatabaseConnection:
    """Simple singleton - only one instance exists"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new database connection...")
            cls._instance = super().__new__(cls)
            cls._instance.connection_count = 0
        else:
            print("Returning existing database connection...")
        return cls._instance

    def connect(self):
        self.connection_count += 1
        return f"Connected (Total connections: {self.connection_count})"

# Try creating multiple instances
db1 = DatabaseConnection()
print(db1.connect())

db2 = DatabaseConnection()
print(db2.connect())

db3 = DatabaseConnection()
print(db3.connect())

print(f"\nAre db1 and db2 the same object? {db1 is db2}")
print(f"Are db2 and db3 the same object? {db2 is db3}")


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("BEGINNER OOP CONCEPTS - SUMMARY")
print("="*70)
print("""
You've learned:
✅ 1.  Basic classes and objects
✅ 2.  Class and instance attributes
✅ 3.  Instance methods
✅ 4.  The __init__ constructor
✅ 5.  Understanding 'self'
✅ 6.  Class methods (@classmethod)
✅ 7.  Static methods (@staticmethod)
✅ 8.  Encapsulation (public, protected, private)
✅ 9.  Property decorators (@property)
✅ 10. String representation (__str__, __repr__)
✅ 11. Class vs instance variables
✅ 12. Method chaining
✅ 13. Object comparison
✅ 14. Making classes iterable
✅ 15. Context managers
✅ 16. Callable objects
✅ 17. Getters and setters
✅ 18. Documentation
✅ 19. Dynamic attribute management
✅ 20. Singleton pattern

Next: Intermediate OOP concepts (Inheritance, Polymorphism, etc.)
""")
