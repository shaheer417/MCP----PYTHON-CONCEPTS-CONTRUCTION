"""
OBJECT-ORIENTED PROGRAMMING (OOP) - INTERMEDIATE LEVEL
=======================================================

Advanced OOP concepts essential for MCP development - Part 2

Topics Covered:
1. Inheritance (Single, Multiple)
2. Method Overriding
3. Super() Function
4. Polymorphism
5. Abstract Base Classes (ABC)
6. Composition vs Inheritance
7. Mixins
8. Operator Overloading
9. Descriptors
10. Type Hints with Classes

These concepts are crucial for understanding MCP server/client architecture!
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Protocol
from dataclasses import dataclass
import json

# ============================================================================
# EXAMPLE 1: Single Inheritance
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 1: Single Inheritance")
print("="*70)

class Vehicle:
    """Base class"""
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.is_running = False

    def start(self):
        self.is_running = True
        return f"{self.brand} {self.model} started"

    def stop(self):
        self.is_running = False
        return f"{self.brand} {self.model} stopped"

class ElectricCar(Vehicle):
    """Derived class"""
    def __init__(self, brand, model, battery_capacity):
        super().__init__(brand, model)  # Call parent constructor
        self.battery_capacity = battery_capacity
        self.battery_level = 100

    def charge(self, amount):
        self.battery_level = min(100, self.battery_level + amount)
        return f"Charged to {self.battery_level}%"

# Usage
tesla = ElectricCar("Tesla", "Model 3", 75)
print(tesla.start())  # Inherited method
print(tesla.charge(20))  # New method
print(f"Battery: {tesla.battery_capacity} kWh, Level: {tesla.battery_level}%")


# ============================================================================
# EXAMPLE 2: Method Overriding
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 2: Method Overriding")
print("="*70)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def info(self):
        return f"I am {self.name}"

class Dog(Animal):
    def speak(self):  # Override parent method
        return f"{self.name} barks: Woof!"

class Cat(Animal):
    def speak(self):  # Override parent method
        return f"{self.name} meows: Meow!"

# Polymorphism in action
animals = [
    Animal("Generic Animal"),
    Dog("Buddy"),
    Cat("Whiskers")
]

for animal in animals:
    print(animal.speak())


# ============================================================================
# EXAMPLE 3: Using super() in Depth
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 3: Understanding super()")
print("="*70)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"I'm {self.name}, {self.age} years old"

class Student(Person):
    def __init__(self, name, age, student_id, major):
        super().__init__(name, age)  # Call parent __init__
        self.student_id = student_id
        self.major = major

    def introduce(self):
        # Extend parent method
        base_intro = super().introduce()
        return f"{base_intro}. Student ID: {self.student_id}, Major: {self.major}"

class GraduateStudent(Student):
    def __init__(self, name, age, student_id, major, thesis_topic):
        super().__init__(name, age, student_id, major)
        self.thesis_topic = thesis_topic

    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro}. Thesis: {thesis_topic}"

student = Student("Alice", 20, "S12345", "Computer Science")
print(student.introduce())

thesis_topic = "Machine Learning in Healthcare"
grad = GraduateStudent("Bob", 25, "G67890", "AI Research", thesis_topic)
print(grad.introduce())


# ============================================================================
# EXAMPLE 4: Multiple Inheritance
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 4: Multiple Inheritance")
print("="*70)

class Flyable:
    def fly(self):
        return f"{self.name} is flying"

class Swimmable:
    def swim(self):
        return f"{self.name} is swimming"

class Duck(Animal, Flyable, Swimmable):
    """Duck inherits from multiple classes"""
    def __init__(self, name):
        Animal.__init__(self, name)

    def speak(self):
        return f"{self.name} quacks: Quack!"

duck = Duck("Donald")
print(duck.speak())  # From Duck (overrides Animal)
print(duck.fly())    # From Flyable
print(duck.swim())   # From Swimmable


# ============================================================================
# EXAMPLE 5: Method Resolution Order (MRO)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 5: Method Resolution Order (MRO)")
print("="*70)

class A:
    def process(self):
        return "A"

class B(A):
    def process(self):
        return "B"

class C(A):
    def process(self):
        return "C"

class D(B, C):
    pass

d = D()
print(f"D.process() returns: {d.process()}")
print(f"MRO for class D: {[cls.__name__ for cls in D.__mro__]}")
# MRO: D -> B -> C -> A -> object


# ============================================================================
# EXAMPLE 6: Abstract Base Classes (ABC)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 6: Abstract Base Classes")
print("="*70)

class Shape(ABC):
    """Abstract base class - cannot be instantiated"""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        """Must be implemented by subclasses"""
        pass

    @abstractmethod
    def perimeter(self):
        """Must be implemented by subclasses"""
        pass

    def describe(self):
        """Concrete method - can be used as is"""
        return f"I am a {self.name}"

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# shape = Shape("test")  # Error! Can't instantiate abstract class
circle = Circle(5)
rect = Rectangle(4, 6)

print(f"{circle.describe()}: Area = {circle.area():.2f}, Perimeter = {circle.perimeter():.2f}")
print(f"{rect.describe()}: Area = {rect.area()}, Perimeter = {rect.perimeter()}")


# ============================================================================
# EXAMPLE 7: Composition over Inheritance
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 7: Composition Pattern")
print("="*70)

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
        self.is_running = False

    def start(self):
        self.is_running = True
        return "Engine started"

    def stop(self):
        self.is_running = False
        return "Engine stopped"

class Transmission:
    def __init__(self, gears):
        self.gears = gears
        self.current_gear = 1

    def shift_up(self):
        if self.current_gear < self.gears:
            self.current_gear += 1
        return f"Shifted to gear {self.current_gear}"

    def shift_down(self):
        if self.current_gear > 1:
            self.current_gear -= 1
        return f"Shifted to gear {self.current_gear}"

class Car:
    """Car HAS-A Engine and Transmission (composition)"""
    def __init__(self, brand, model, horsepower, gears):
        self.brand = brand
        self.model = model
        self.engine = Engine(horsepower)  # Composition
        self.transmission = Transmission(gears)  # Composition

    def start(self):
        return f"{self.brand} {self.model}: {self.engine.start()}"

    def accelerate(self):
        if self.engine.is_running:
            return self.transmission.shift_up()
        return "Start the engine first!"

car = Car("Honda", "Civic", 180, 6)
print(car.start())
print(car.accelerate())
print(car.accelerate())


# ============================================================================
# EXAMPLE 8: Mixins
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 8: Mixins Pattern")
print("="*70)

class JSONMixin:
    """Mixin to add JSON serialization capability"""
    def to_json(self):
        return json.dumps(self.__dict__, indent=2)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

class ReprMixin:
    """Mixin to add nice __repr__"""
    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class User(JSONMixin, ReprMixin):
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

user = User("john_doe", "john@example.com", 30)
print(f"User repr: {repr(user)}")
print(f"User JSON:\n{user.to_json()}")

# Deserialize
json_str = '{"username": "jane_doe", "email": "jane@example.com", "age": 25}'
user2 = User.from_json(json_str)
print(f"Deserialized: {repr(user2)}")


# ============================================================================
# EXAMPLE 9: Operator Overloading
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 9: Operator Overloading")
print("="*70)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Overload + operator"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Overload - operator"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Overload * operator"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """Overload == operator"""
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"v1 == v2: {v1 == v2}")


# ============================================================================
# EXAMPLE 10: Descriptors
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 10: Descriptors")
print("="*70)

class PositiveNumber:
    """Descriptor that enforces positive numbers"""

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} must be positive")
        obj.__dict__[self.name] = value

class Product:
    price = PositiveNumber("price")
    quantity = PositiveNumber("quantity")

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price  # Uses descriptor
        self.quantity = quantity  # Uses descriptor

    def total_value(self):
        return self.price * self.quantity

product = Product("Laptop", 1000, 5)
print(f"{product.name}: ${product.price} x {product.quantity} = ${product.total_value()}")

try:
    product.price = -100  # Will raise ValueError
except ValueError as e:
    print(f"Error: {e}")


# ============================================================================
# EXAMPLE 11: Property with Validation
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 11: Advanced Property Usage")
print("="*70)

class Email:
    def __init__(self, address):
        self._address = None
        self.address = address  # Uses setter

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if '@' not in value:
            raise ValueError("Invalid email address")
        self._address = value

    @property
    def domain(self):
        return self._address.split('@')[1]

    @property
    def username(self):
        return self._address.split('@')[0]

email = Email("john@example.com")
print(f"Full address: {email.address}")
print(f"Username: {email.username}")
print(f"Domain: {email.domain}")

try:
    email.address = "invalid_email"  # Will raise ValueError
except ValueError as e:
    print(f"Error: {e}")


# ============================================================================
# EXAMPLE 12: Class Inheritance with Type Hints
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 12: Type Hints with Classes")
print("="*70)

class Database:
    def __init__(self, name: str):
        self.name: str = name
        self.connections: int = 0

    def connect(self) -> str:
        self.connections += 1
        return f"Connected to {self.name}"

    def disconnect(self) -> str:
        if self.connections > 0:
            self.connections -= 1
        return f"Disconnected from {self.name}"

    def get_status(self) -> dict[str, Union[str, int]]:
        return {
            "name": self.name,
            "connections": self.connections
        }

db = Database("PostgreSQL")
print(db.connect())
print(db.get_status())


# ============================================================================
# EXAMPLE 13: Protocol (Structural Subtyping)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 13: Protocol (Duck Typing with Type Hints)")
print("="*70)

class Drawable(Protocol):
    """Protocol defines an interface"""
    def draw(self) -> str:
        ...

class Square:
    def __init__(self, size):
        self.size = size

    def draw(self) -> str:
        return f"Drawing a square of size {self.size}"

class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def draw(self) -> str:
        return f"Drawing a triangle (base={self.base}, height={self.height})"

def render(shape: Drawable) -> None:
    """Function accepts any object with draw() method"""
    print(shape.draw())

# Both work because they implement draw()
square = Square(10)
triangle = Triangle(5, 8)

render(square)
render(triangle)


# ============================================================================
# EXAMPLE 14: Dataclass with Inheritance
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 14: Dataclasses with Inheritance")
print("="*70)

@dataclass
class BaseConfig:
    app_name: str
    version: str

@dataclass
class ServerConfig(BaseConfig):
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

config = ServerConfig(
    app_name="MyApp",
    version="1.0.0",
    host="0.0.0.0",
    port=3000
)

print(f"Config: {config}")
print(f"URL: {config.get_url()}")


# ============================================================================
# EXAMPLE 15: Factory Pattern with Class Methods
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 15: Factory Pattern")
print("="*70)

class Connection:
    def __init__(self, host: str, port: int, protocol: str):
        self.host = host
        self.port = port
        self.protocol = protocol

    @classmethod
    def http_connection(cls, host: str) -> 'Connection':
        """Factory method for HTTP"""
        return cls(host, 80, "HTTP")

    @classmethod
    def https_connection(cls, host: str) -> 'Connection':
        """Factory method for HTTPS"""
        return cls(host, 443, "HTTPS")

    @classmethod
    def custom_connection(cls, host: str, port: int) -> 'Connection':
        """Factory method for custom connection"""
        return cls(host, port, "CUSTOM")

    def __str__(self):
        return f"{self.protocol}://{self.host}:{self.port}"

# Using factory methods
http_conn = Connection.http_connection("example.com")
https_conn = Connection.https_connection("secure.com")
custom_conn = Connection.custom_connection("api.example.com", 8080)

print(http_conn)
print(https_conn)
print(custom_conn)


# ============================================================================
# EXAMPLE 16: Observer Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 16: Observer Pattern")
print("="*70)

class Subject:
    """Subject that notifies observers"""
    def __init__(self):
        self._observers: List['Observer'] = []
        self._state: str = ""

    def attach(self, observer: 'Observer') -> None:
        self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state: str) -> None:
        self._state = state
        self.notify()

class Observer(ABC):
    """Abstract observer"""
    @abstractmethod
    def update(self, state: str) -> None:
        pass

class EmailNotifier(Observer):
    def update(self, state: str) -> None:
        print(f"Email Notifier: Sending email about '{state}'")

class SMSNotifier(Observer):
    def update(self, state: str) -> None:
        print(f"SMS Notifier: Sending SMS about '{state}'")

# Usage
subject = Subject()
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()

subject.attach(email_notifier)
subject.attach(sms_notifier)

print("Setting state to 'Order Shipped':")
subject.set_state("Order Shipped")

print("\nSetting state to 'Order Delivered':")
subject.set_state("Order Delivered")


# ============================================================================
# EXAMPLE 17: Strategy Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 17: Strategy Pattern")
print("="*70)

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} using Credit Card ending in {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} using PayPal account {self.email}"

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        return f"Paid ${amount} using Crypto wallet {self.wallet_address[:10]}..."

class ShoppingCart:
    def __init__(self):
        self.items: List[tuple[str, float]] = []
        self.payment_strategy: Optional[PaymentStrategy] = None

    def add_item(self, item: str, price: float) -> None:
        self.items.append((item, price))

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self.payment_strategy = strategy

    def checkout(self) -> str:
        total = sum(price for _, price in self.items)
        if not self.payment_strategy:
            return "Please set a payment method"
        return self.payment_strategy.pay(total)

# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 1000)
cart.add_item("Mouse", 25)

cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
print(cart.checkout())

cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())


# ============================================================================
# EXAMPLE 18: Decorator Pattern (Not Python decorators!)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 18: Decorator Pattern (Design Pattern)")
print("="*70)

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Simple coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + ", milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return self._coffee.description() + ", sugar"

# Building a coffee
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost()}")

coffee_with_milk = MilkDecorator(coffee)
print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost()}")

coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)
print(f"{coffee_with_milk_and_sugar.description()}: ${coffee_with_milk_and_sugar.cost()}")


# ============================================================================
# EXAMPLE 19: Command Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 19: Command Pattern")
print("="*70)

class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> str:
        pass

class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self) -> str:
        self.is_on = True
        return "Light is ON"

    def turn_off(self) -> str:
        self.is_on = False
        return "Light is OFF"

class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self) -> str:
        return self.light.turn_on()

    def undo(self) -> str:
        return self.light.turn_off()

class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self) -> str:
        return self.light.turn_off()

    def undo(self) -> str:
        return self.light.turn_on()

class RemoteControl:
    def __init__(self):
        self.command: Optional[Command] = None

    def set_command(self, command: Command) -> None:
        self.command = command

    def press_button(self) -> str:
        if self.command:
            return self.command.execute()
        return "No command set"

    def press_undo(self) -> str:
        if self.command:
            return self.command.undo()
        return "No command to undo"

# Usage
light = Light()
light_on = LightOnCommand(light)
light_off = LightOffCommand(light)

remote = RemoteControl()

remote.set_command(light_on)
print(remote.press_button())  # Turn on
print(remote.press_undo())    # Undo (turn off)

remote.set_command(light_off)
print(remote.press_button())  # Turn off
print(remote.press_undo())    # Undo (turn on)


# ============================================================================
# EXAMPLE 20: MCP-Like Architecture Example
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 20: MCP-Like Architecture (Simplified)")
print("="*70)

class Tool(ABC):
    """Abstract base for MCP tools"""
    @abstractmethod
    def execute(self, **kwargs) -> dict:
        pass

class ReadFileTool(Tool):
    def execute(self, **kwargs) -> dict:
        filepath = kwargs.get('filepath', '')
        return {
            "tool": "read_file",
            "status": "success",
            "result": f"Contents of {filepath}"
        }

class WriteFileTool(Tool):
    def execute(self, **kwargs) -> dict:
        filepath = kwargs.get('filepath', '')
        content = kwargs.get('content', '')
        return {
            "tool": "write_file",
            "status": "success",
            "result": f"Wrote {len(content)} bytes to {filepath}"
        }

class MCPServer:
    """Simplified MCP Server"""
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, Tool] = {}

    def register_tool(self, name: str, tool: Tool) -> None:
        self.tools[name] = tool
        print(f"Registered tool: {name}")

    def call_tool(self, tool_name: str, **kwargs) -> dict:
        if tool_name not in self.tools:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
        return self.tools[tool_name].execute(**kwargs)

class MCPClient:
    """Simplified MCP Client"""
    def __init__(self, server: MCPServer):
        self.server = server

    def request(self, tool_name: str, **kwargs) -> dict:
        print(f"Client requesting: {tool_name}")
        response = self.server.call_tool(tool_name, **kwargs)
        print(f"Server response: {response}")
        return response

# Usage
server = MCPServer("FileServer")
server.register_tool("read_file", ReadFileTool())
server.register_tool("write_file", WriteFileTool())

client = MCPClient(server)
client.request("read_file", filepath="/data/document.txt")
client.request("write_file", filepath="/data/output.txt", content="Hello MCP!")


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("INTERMEDIATE OOP CONCEPTS - SUMMARY")
print("="*70)
print("""
You've learned:
✅ 1.  Single inheritance
✅ 2.  Method overriding
✅ 3.  Using super()
✅ 4.  Multiple inheritance
✅ 5.  Method Resolution Order (MRO)
✅ 6.  Abstract Base Classes (ABC)
✅ 7.  Composition over inheritance
✅ 8.  Mixins
✅ 9.  Operator overloading
✅ 10. Descriptors
✅ 11. Advanced properties
✅ 12. Type hints with classes
✅ 13. Protocols (structural subtyping)
✅ 14. Dataclasses with inheritance
✅ 15. Factory pattern
✅ 16. Observer pattern
✅ 17. Strategy pattern
✅ 18. Decorator pattern
✅ 19. Command pattern
✅ 20. MCP-like architecture

Next: Advanced OOP concepts (Metaclasses, Advanced Patterns, etc.)
""")
