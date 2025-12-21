# Task 5
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    def euclidian_distance(self, other):
        if not isinstance(other, Point):
            return TypeError("Please provide a valid point to compare.")
        dist_x = other.x - self.x
        dist_y = other.y - self.y
        
        return math.sqrt(dist_x**2 + dist_y**2)
        
class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
        
    def __add__(self, other):
        if not isinstance(other, Vector):
            return TypeError("Please provide a valid Vector to add")
        sum_x = self.x + other.x
        sum_y = self.y + other.y
        
        return Vector(sum_x, sum_y)

# Demonstrates the Point class.
p1 = Point(2, 4)
p2 = Point(2, 4)
p3 = Point(5, 7)

# __str__
print(f"Point 1 is {p1}")
print(f"Point 2 is {p2}")
print(f"Point 3 is {p3}")

# __eq__

print(f"Point 1 is equal to Point 2: {p1 == p2}")
print(f"Point 1 is equal to Point 3: {p1 == p3}")

# Euclidean Distance
print(f"The Euclidean Distance from Point 1 to Point 3 is {p1.euclidian_distance(p3): .2f}")

# Demonstrates the Vector class
v1 = Vector(2, 4)
v2 = Vector(3, 5)

# __str__
print(f"Vector 1 is {v1}")
print(f"Vector 2 is {v2}")

# __add__
print(f"Vector 1 plus Vector 2 is {v1 + v2}")

# __eq__ (inherited from Point class)
print(f"Vector 1 is equal to Vector 2: {v1 == v2}")