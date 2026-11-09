from math import isqrt, prod

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algorithms.factoring import fermat_factor, fermat_factorize


def is_prime(n: int) -> bool:
    """Reference primality test by plain trial division."""
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


def closest_divisor_pair(n: int) -> tuple[int, int]:
    """Reference: the divisor pair (p, q), p <= q, with p as large as possible."""
    p = next(d for d in range(isqrt(n), 0, -1) if n % d == 0)
    return (p, n // p)


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (5959, (59, 101)),  # classic textbook example
        (8051, (83, 97)),
        (15, (3, 5)),
        (21, (3, 7)),
        (9, (3, 3)),  # perfect square: found on the first step
        (49, (7, 7)),
        (1_000_003 * 1_000_033, (1_000_003, 1_000_033)),  # close primes, fast
        (45, (5, 9)),  # closest pair, not necessarily prime factors
    ],
)
def test_known_factorizations(n, expected):
    assert fermat_factor(n) == expected


@pytest.mark.parametrize("p", [3, 5, 7, 97, 7919, 104_729])
def test_prime_returns_trivial_pair(p):
    assert fermat_factor(p) == (1, p)


def test_one_and_two():
    assert fermat_factor(1) == (1, 1)
    assert fermat_factor(2) == (1, 2)


@pytest.mark.parametrize(
    ("n", "expected"), [(4, (2, 2)), (10, (2, 5)), (1024, (2, 512))]
)
def test_even_input_splits_off_two(n, expected):
    assert fermat_factor(n) == expected


def test_large_close_factors_are_fast():
    # Two 31-digit primes that differ by a small amount: one Fermat step.
    p = 1_000_000_000_000_000_000_000_000_000_057
    q = 1_000_000_000_000_000_000_000_000_000_099
    assert fermat_factor(p * q, max_iterations=10) == (p, q)


def test_max_iterations_raises_when_exceeded():
    # 3 * 1_000_003 needs about n/6 steps; 10 is far too few.
    with pytest.raises(RuntimeError):
        fermat_factor(3 * 1_000_003, max_iterations=10)


def test_max_iterations_zero_allows_immediate_hit():
    assert fermat_factor(49, max_iterations=0) == (7, 7)


@pytest.mark.parametrize("bad", [0, -1, -15])
def test_rejects_non_positive(bad):
    with pytest.raises(ValueError):
        fermat_factor(bad)
    with pytest.raises(ValueError):
        fermat_factorize(bad)


@pytest.mark.parametrize("bad", [15.0, "15", None, True])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        fermat_factor(bad)


def test_rejects_negative_max_iterations():
    with pytest.raises(ValueError):
        fermat_factor(15, max_iterations=-1)


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, []),
        (2, [2]),
        (97, [97]),
        (360, [2, 2, 2, 3, 3, 5]),
        (5959, [59, 101]),
        (3**5 * 7**2, [3, 3, 3, 3, 3, 7, 7]),
    ],
)
def test_factorize_known(n, expected):
    assert fermat_factorize(n) == expected


# Property-based tests against the brute-force references above.


@given(st.integers(min_value=1, max_value=200_000).map(lambda k: 2 * k + 1))
def test_odd_matches_closest_divisor_pair(n):
    assert fermat_factor(n) == closest_divisor_pair(n)


@given(st.integers(min_value=1, max_value=10**6))
def test_factor_pair_is_valid(n):
    p, q = fermat_factor(n)
    assert p * q == n
    assert 1 <= p <= q
    assert (p == 1) == (n == 1 or is_prime(n))


@given(st.integers(min_value=1, max_value=10**5))
def test_factorize_product_and_primality(n):
    factors = fermat_factorize(n)
    assert prod(factors) == n
    assert all(is_prime(f) for f in factors)
    assert factors == sorted(factors)
