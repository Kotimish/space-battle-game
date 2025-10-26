import math


class Angle:
    def __init__(self, direction: int, directions_number: int) -> None:
        self.direction = direction
        self.directions_number = directions_number

    def __add__(self, other: 'Angle') -> 'Angle':
        if not isinstance(other, Angle):
            raise TypeError(f"Expected Angle object, received {type(other).__name__}")
        if self.directions_number != other.directions_number:  # noqa: SLF001
            raise ValueError(
                f'Trying to add {self} and {other} with different number directions'
            )
        new_direction = (self.direction + other.direction) % self.directions_number
        return Angle(new_direction, self.directions_number)

    def __eq__(self, other):
        if not isinstance(other, Angle):
            raise TypeError(f"Expected Angle object, received {type(other).__name__}")
        return (
            self.direction == other.direction and
            self.directions_number == self.directions_number
        )

    def __str__(self) -> str:
        return f'Angle({self.direction}/{self.directions_number})'

    def get_degrees(self) -> float:
        return (360 / self.directions_number) * self.direction

    def get_radians(self) -> float:
        return (2 * math.pi / self.directions_number) * self.direction

    def to_dict(self) -> dict[str, int]:
        return {
            "direction": self.direction,
            "directions_number": self.directions_number,
        }

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> 'Angle':
        return cls(
            direction=data["direction"],
            directions_number=data["directions_number"],
        )
