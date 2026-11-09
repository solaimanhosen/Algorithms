"""Trial division, in three variants.

Trial division tries candidate divisors ``d = 2, 3, ...`` in increasing
order. Each time ``d`` divides the remaining number ``m``, it is divided out
and recorded. The search stops once ``d² > m``: at that point ``m`` has no
factor ``<= √m`` left, so ``m`` is 1 or prime.

Because candidates are tried smallest first, every ``d`` that divides ``m``
is prime: all its own prime factors were already divided out.

The variants differ only in which candidates they try, up to √n:

* :func:`trial_division`: every integer, so about √n divisions.
  No extra time or memory.
* :func:`trial_division_wheel`: only integers coprime to 2·3·5, so about
  √n / 3.75 divisions. No extra time or memory.
* :func:`trial_division_primes`: only primes, so about 2√n / ln n divisions
  (prime number theorem). Generating the primes costs about as much time
  as the divisions it saves, plus O(n^(1/4)) memory for a segmented sieve.

All three are O(√n) time in the worst case (``n`` prime, or a product of two
primes near √n), and O(p) to find a smallest prime factor ``p``. The
prime-table variant pays off when one table is reused for many numbers; pass
it in as ``primes``.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import cycle
from math import isqrt

from algorithms._validation import check_positive_int
from algorithms.primes import iter_primes

# Gaps between consecutive integers coprime to 2·3·5 = 30, starting at 7:
# 7, 11, 13, 17, 19, 23, 29, 31, 37, ... (8 of every 30 integers).
_WHEEL_30_GAPS = (4, 2, 4, 2, 4, 6, 2, 6)


def trial_division(n: int) -> list[int]:
    """Return the prime factorization of ``n``, trying every integer as a divisor.

    The simplest form: try 2, 3, 4, 5, ... up to √m.

    Examples:
        >>> trial_division(360)
        [2, 2, 2, 3, 3, 5]
        >>> trial_division(97)
        [97]
        >>> trial_division(1)
        []
    """
    m = check_positive_int(n)
    factors: list[int] = []
    d = 2
    while d * d <= m:
        while m % d == 0:
            factors.append(d)
            m //= d
        d += 1
    if m > 1:
        factors.append(m)
    return factors


def trial_division_wheel(n: int) -> list[int]:
    """Return the prime factorization of ``n`` using a 2·3·5 wheel.

    After dividing out 2, 3 and 5, only numbers coprime to 30 can be prime,
    so it skips the rest. That is 8 candidates in every 30 instead of 30,
    about 3.75 times fewer divisions than :func:`trial_division`.

    Examples:
        >>> trial_division_wheel(360)
        [2, 2, 2, 3, 3, 5]
        >>> trial_division_wheel(7 * 49 * 101)
        [7, 7, 7, 101]
    """
    m = check_positive_int(n)
    factors: list[int] = []
    for p in (2, 3, 5):
        while m % p == 0:
            factors.append(p)
            m //= p
    d = 7
    for gap in cycle(_WHEEL_30_GAPS):
        if d * d > m:
            break
        while m % d == 0:
            factors.append(d)
            m //= d
        d += gap
    if m > 1:
        factors.append(m)
    return factors


def trial_division_primes(n: int, primes: Iterable[int] | None = None) -> list[int]:
    """Return the prime factorization of ``n``, dividing only by primes.

    Args:
        n: The positive integer to factor.
        primes: Optional increasing sequence of primes starting at 2 with no
            gaps, for example ``primes_up_to(10**6)`` reused across many
            calls. If it runs out before √m (``m`` being the cofactor still
            left), the search carries on past it with plain division, so
            the result is always correct. By default primes are generated
            lazily with a segmented sieve, so the search can stop as soon as
            the cofactor is small.

    Examples:
        >>> trial_division_primes(360)
        [2, 2, 2, 3, 3, 5]
        >>> from algorithms.primes import primes_up_to
        >>> table = primes_up_to(100)
        >>> trial_division_primes(9991, primes=table)
        [97, 103]
    """
    m = check_positive_int(n)
    source = iter_primes(isqrt(m)) if primes is None else primes
    factors: list[int] = []
    largest_tried = 1
    for p in source:
        if p * p > m:
            break
        while m % p == 0:
            factors.append(p)
            m //= p
        largest_tried = p
    else:
        # The primes ran out before passing √m. Every prime up to
        # largest_tried is divided out, so continue with plain division.
        d = largest_tried + 1
        while d * d <= m:
            while m % d == 0:
                factors.append(d)
                m //= d
            d += 1
    if m > 1:
        factors.append(m)
    return factors
