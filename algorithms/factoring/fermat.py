"""Fermat's factorization method.

Every odd integer ``n`` can be written as a difference of two squares::

    n = a² - b² = (a - b)(a + b)

If ``n = p·q`` with ``p <= q`` both odd, then ``a = (p + q) / 2`` and
``b = (q - p) / 2``. Fermat's method starts at ``a = ceil(√n)`` and steps
``a`` up by one until ``a² - n`` is a perfect square ``b²``. It then returns
the factor pair ``(a - b, a + b)``.

Complexity
----------
* Time: about ``(p + q)/2 - √n`` iterations, each one an integer square
  root. This is very fast when ``p`` and ``q`` are close to ``√n`` (one step
  when ``n`` is a perfect square). It is O(n) in the worst case, when ``n``
  has a tiny factor: for ``n = 3q`` it takes about ``n/6`` steps. For a prime
  ``n`` it runs to ``a = (n + 1)/2`` and returns ``(1, n)``.
* Memory: O(1) integers, each O(log n) bits.

Fermat's method only works on odd ``n``. Even inputs are split as
``(2, n // 2)`` directly.
"""

from __future__ import annotations

from math import isqrt

from algorithms._validation import check_positive_int

# Quadratic residues modulo 64: a perfect square must leave one of these
# remainders. Checking this first skips the comparatively costly isqrt()
# for about 81% of non-squares.
_SQUARES_MOD_64 = frozenset(i * i % 64 for i in range(64))


def _is_square(x: int) -> bool:
    """Return True if ``x`` (assumed >= 0) is a perfect square."""
    if x & 63 not in _SQUARES_MOD_64:
        return False
    r = isqrt(x)
    return r * r == x


def fermat_factor(n: int, max_iterations: int | None = None) -> tuple[int, int]:
    """Split ``n`` into two factors ``(p, q)`` with ``p * q == n`` and ``p <= q``.

    For odd ``n`` this returns the factor pair closest to ``√n``. The result
    is ``(1, n)`` exactly when ``n`` is 1 or prime. For even ``n`` it returns
    ``(2, n // 2)``.

    Args:
        n: The positive integer to factor.
        max_iterations: Optional cap on the number of values of ``a`` tried.
            If the cap is reached before a factor is found, ``RuntimeError``
            is raised. ``None`` (the default) means no cap.

    Raises:
        TypeError: If ``n`` is not an int.
        ValueError: If ``n`` is not positive, or ``max_iterations`` is negative.
        RuntimeError: If ``max_iterations`` is reached.

    Examples:
        >>> fermat_factor(5959)
        (59, 101)
        >>> fermat_factor(97)
        (1, 97)
    """
    n = check_positive_int(n)
    if max_iterations is not None and max_iterations < 0:
        raise ValueError("max_iterations must be non-negative")

    if n % 2 == 0:
        return (2, n // 2) if n > 2 else (1, 2)

    a = isqrt(n)
    if a * a < n:
        a += 1  # a = ceil(√n)
    b2 = a * a - n

    # Update b² = a² - n incrementally: (a + 1)² - a² = 2a + 1.
    # For odd n the loop always ends, at the latest at a = (n + 1)/2,
    # where b = (n - 1)/2 gives the trivial pair (1, n).
    iterations = 0
    while not _is_square(b2):
        if max_iterations is not None and iterations >= max_iterations:
            raise RuntimeError(
                f"no factor found for {n} within {max_iterations} iterations"
            )
        b2 += 2 * a + 1
        a += 1
        iterations += 1

    b = isqrt(b2)
    return (a - b, a + b)


def fermat_factorize(n: int) -> list[int]:
    """Return the prime factorization of ``n`` as a sorted list.

    Splits ``n`` repeatedly with :func:`fermat_factor` until every part is
    prime. ``fermat_factorize(1)`` returns ``[]``.

    This inherits Fermat's O(n) worst case, so it is only practical for
    small inputs or numbers whose factors are close together.

    Examples:
        >>> fermat_factorize(360)
        [2, 2, 2, 3, 3, 5]
    """
    n = check_positive_int(n)
    primes: list[int] = []
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        p, q = fermat_factor(m)
        if p == 1:
            primes.append(q)  # m is prime
        else:
            stack.extend((p, q))
    return sorted(primes)
