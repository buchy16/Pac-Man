"""Vector utilities used for 2D movement and projectile direction."""

from math import sqrt, acos, degrees
from typing import Any, Tuple


class Vector():
    """Represent a 2D vector and basic vector operations."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize vector coordinates.

        Args:
            x: Horizontal component.
            y: Vertical component.
        """
        self.x = x
        self.y = y

    def __str__(self):
        """Return a readable representation of the vector."""
        return f"({self.x}, {self.y})"

    def __mul__(self, other: Any) -> "Vector":
        """Multiply vector components by a scalar or another vector.

        Args:
            other: Scalar value or vector used for component-wise product.

        Returns:
            Vector: The resulting multiplied vector.
        """
        if (isinstance(other, Vector)):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other: Any) -> "Vector":
        """Divide vector components by a scalar or another vector.

        Args:
            other: Scalar value or vector used for component-wise division.

        Returns:
            Vector: The resulting divided vector.
        """
        if (isinstance(other, Vector)):
            return Vector(self.x / other.x, self.y / other.y)
        else:
            return Vector(self.x / other, self.y / other)

    def __add__(self, other: Any) -> "Vector":
        """Add another vector component-wise.

        Args:
            other: Vector to add.

        Returns:
            Vector: The resulting vector.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any) -> "Vector":
        """Subtract another vector component-wise.

        Args:
            other: Vector to subtract.

        Returns:
            Vector: The resulting vector.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def norm(self) -> float:
        """Compute the Euclidean norm of the vector.

        Returns:
            float: Length of the vector.
        """
        return (sqrt(self.x ** 2 + self.y ** 2))

    def unit_vector(self) -> "Vector":
        """Return the normalized vector with magnitude 1.

        Returns:
            Vector: Unit vector in the same direction.
        """
        norm = self.norm()
        return self / norm

    def apply(self,
              point: Tuple[float, float]) -> Tuple[float, float]:
        """Translate a point by the vector components.

        Args:
            point: Point to translate as ``(x, y)``.

        Returns:
            Tuple[float, float]: Translated point.
        """
        return (point[0] + self.x, point[1] + self.y)

    def get_angle(self, v2: "Vector") -> float:
        uv = (self.x * v2.x) + (self.y * v2.y)
        cosθ = uv / (self.norm() * v2.norm())
        return (degrees(acos(cosθ)))


if (__name__ == "__main__"):
    v1 = Vector(-2, 0)
    v2 = Vector(0, -2)

    print(v1.get_angle(v2))
