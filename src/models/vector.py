
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise TypeError(f"Expected Vector object, received {type(other).__name__}")
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'Vector({self.x}, {self.y})'

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"Expected Vector object, received {type(other).__name__}")
        return (
            self.x == other.x and
            self.y == other.y
        )
