"""Input checks shared across the package."""

from __future__ import annotations


def check_positive_int(n: object, name: str = "n") -> int:
    """Return ``n`` if it is a positive int, otherwise raise.

    Raises:
        TypeError: If ``n`` is not an int. ``bool`` is rejected even though it
            is a subclass of ``int``.
        ValueError: If ``n`` is less than 1.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"{name} must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"{name} must be a positive integer, got {n}")
    return n


def check_non_negative_int(n: object, name: str = "n") -> int:
    """Return ``n`` if it is an int >= 0, otherwise raise TypeError/ValueError."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"{name} must be an int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"{name} must be non-negative, got {n}")
    return n
