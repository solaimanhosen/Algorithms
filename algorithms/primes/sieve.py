"""Sieve of Eratosthenes, in a plain and a segmented form.

The sieve marks every multiple of each prime ``p`` (starting at ``p²``) as
composite. Whatever stays unmarked is prime.

* :func:`primes_up_to` sieves ``[0, limit]`` in one array.
  Time O(limit · log log limit), memory O(limit) bytes.
* :func:`iter_primes` sieves the range in fixed-size segments and yields
  primes lazily. Same time, but memory is only O(√limit): the primes up to
  √limit plus one segment. Because it is lazy, a caller can stop early and
  skip the remaining work.
"""

from __future__ import annotations

from collections.abc import Iterator
from math import isqrt

from algorithms._validation import check_non_negative_int


def primes_up_to(limit: int) -> list[int]:
    """Return all primes ``p`` with ``p <= limit``, in increasing order.

    Examples:
        >>> primes_up_to(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        >>> primes_up_to(1)
        []
    """
    limit = check_non_negative_int(limit, "limit")
    if limit < 2:
        return []
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            # Smaller multiples of p were already marked by smaller primes.
            is_prime[p * p :: p] = bytes(len(range(p * p, limit + 1, p)))
    return [i for i, flag in enumerate(is_prime) if flag]


def iter_primes(limit: int, segment_size: int | None = None) -> Iterator[int]:
    """Yield all primes ``p <= limit`` in increasing order, using a segmented sieve.

    Nothing is computed ahead of time: each segment is sieved only with
    primes this generator has already yielded. So stopping after the first
    few primes costs almost nothing, even for a huge ``limit``.

    Args:
        limit: Largest number to consider.
        segment_size: Length of each sieved window, default ``2**15``.
            Smaller segments use less memory but add per-segment overhead.

    Examples:
        >>> list(iter_primes(30))
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        >>> list(iter_primes(50, segment_size=8)) == list(iter_primes(50))
        True
    """
    limit = check_non_negative_int(limit, "limit")
    if segment_size is not None:
        segment_size = check_non_negative_int(segment_size, "segment_size")
        if segment_size == 0:
            raise ValueError("segment_size must be positive")
    size = segment_size or 1 << 15
    root = isqrt(limit)

    # Primes <= √limit found so far. Later segments sieve with these, so
    # memory stays O(√limit) however far the generator runs.
    base: list[int] = []

    first = primes_up_to(min(limit, size))
    for p in first:
        yield p
        if p <= root:
            base.append(p)

    low = min(limit, size) + 1
    while low <= limit:
        # Keep high < low², so every prime <= √high is below low and has
        # already been found.
        high = min(low + size - 1, limit, low * low - 1)
        is_prime = bytearray([1]) * (high - low + 1)
        for p in base:
            if p * p > high:
                break
            start = max(p * p, -(-low // p) * p)  # first multiple of p >= low
            is_prime[start - low :: p] = bytes(len(range(start, high + 1, p)))
        for i, flag in enumerate(is_prime):
            if flag:
                q = low + i
                yield q
                if q <= root:
                    base.append(q)
        low = high + 1
