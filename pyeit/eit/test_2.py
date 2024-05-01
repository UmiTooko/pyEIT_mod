from abc import ABC, abstractmethod
import math

# Step 1: Define an abstract class 'Shape'
class Shape(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def calculate_area(self):
        pass

    @abstractmethod
    def calculate_perimeter(self):
        pass



# Step 2: Create concrete subclasses

# Subclass 1: Circle
class Circle(Shape):
    def __init__(self, name, radius):
        super().__init__(name)

        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2

    def calculate_perimeter(self):
        return 2 * math.pi * self.radius
    
    def display_info(self):
        print(f"Shape: {self.name}")
        print(f"Area: {self.calculate_area()}")
        print(f"Perimeter: {self.calculate_perimeter()}")

# Subclass 2: Rectangle
class Rectangle(Shape):
    def __init__(self, name, length, width):
        super().__init__(name)
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)
    
    def display_info(self):
        print(f"Shape: {self.name}")
        print(f"Area: {self.calculate_area()}")
        print(f"Perimeter: {self.calculate_perimeter()}")
# Step 3: Create instances of concrete subclasses
circle = Circle("Circle 1", 5)
rectangle = Rectangle("Rectangle 1", 4, 6)

# Step 4: Use the abstract class methods
circle.display_info()
print("--------------------------")
rectangle.display_info()