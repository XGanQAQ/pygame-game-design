class IntVector2:
    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Coordinates must be integers.")
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, IntVector2):
            raise TypeError("Operand must be an instance of IntVector2.")
        return IntVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, IntVector2):
            raise TypeError("Operand must be an instance of IntVector2.")
        return IntVector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int):
        if not isinstance(scalar, int):
            raise TypeError("Scalar must be an integer.")
        return IntVector2(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        if not isinstance(other, IntVector2):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"IntVector2(x={self.x}, y={self.y})"

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def to_tuple(self):
        return self.x, self.y