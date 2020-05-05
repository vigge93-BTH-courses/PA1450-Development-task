"""Example module."""


def add(a, b):
    """Add two numbers.

    Add two numbers and return the result. Assumes commutative properties.

    Args:
        a: number
        b: number
    Returns:
        The sum of a and b.
    Raises:
        TypeError: If the objects can't be added together.
    """
    return a + b


def multiply(a, b):
    """Multiply two numbers.

    Multiply two numbers together. Assumes commutative properties.

    Args:
        a: number
        b: number
    Returns:
        The product of a and b
    Raises:
        TypeError: If objects do not support multiplication
    """
    return a*b
