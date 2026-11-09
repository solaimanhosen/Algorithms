from math import isqrt, prod

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algorithms.factoring import (
    trial_division,
    trial_division_primes,
    trial_division_wheel,
)
from algorithms.primes import primes_up_to

ALL_VARIANTS = [trial_division, trial_division_wheel, trial_division_primes]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


@pytest.mark.parametrize("factorize", ALL_VARIANTS)
@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, []),
        (2, [2]),
        (3, [3]),
        (4, [2, 2]),
        (30, [2, 3, 5]),
        (49, [7, 7]),  # square of a wheel candidate
        (360, [2, 2, 2, 3, 3, 5]),
        (5959, [59, 101]),
        (2**20, [2] * 20),
        (3**4 * 5**3 * 7**2, [3, 3, 3, 3, 5, 5, 5, 7, 7]),
        (97, [97]),
        (104_729, [104_729]),  # the 10,000th prime
        (1_000_003 * 1_000_033, [1_000_003, 1_000_033]),  # worst case: ~10^6 steps
        (2 * 10**12 + 2, [2, 73, 137, 99_990_001]),
    ],
)
def test_known_factorizations(factorize, n, expected):
    assert factorize(n) == expected


@pytest.mark.parametrize("factorize", ALL_VARIANTS)
def test_large_number_with_small_factors_is_fast(factorize):
    # Huge n, but every factor is tiny, so the cofactor shrinks to 1 quickly.
    n = 2**50 * 3**30 * 7**10
    assert factorize(n) == [2] * 50 + [3] * 30 + [7] * 10


@pytest.mark.parametrize("factorize", ALL_VARIANTS)
@pytest.mark.parametrize("bad", [0, -1, -12])
def test_rejects_non_positive(factorize, bad):
    with pytest.raises(ValueError):
        factorize(bad)


@pytest.mark.parametrize("factorize", ALL_VARIANTS)
@pytest.mark.parametrize("bad", [12.0, "12", None, True])
def test_rejects_non_int(factorize, bad):
    with pytest.raises(TypeError):
        factorize(bad)


def test_reusable_prime_table():
    table = primes_up_to(1000)
    for n in [999_983, 997 * 991, 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19, 1]:
        assert trial_division_primes(n, primes=table) == trial_division(n)


def test_prime_table_can_be_a_one_shot_iterator():
    assert trial_division_primes(5959, primes=iter(primes_up_to(100))) == [59, 101]


def test_prime_table_too_small_falls_back_to_plain_division():
    # 101 * 103 needs primes up to 101; the table stops at 97.
    assert trial_division_primes(101 * 103, primes=primes_up_to(100)) == [101, 103]
    assert trial_division_primes(10_007**2, primes=[2, 3, 5]) == [10_007, 10_007]
    assert trial_division_primes(5959, primes=[]) == [59, 101]


def test_prime_table_small_but_sufficient_for_cofactor():
    # 2**10 * 101: once the 2s are gone, only primes up to 10 are needed.
    assert trial_division_primes(2**10 * 101, primes=[2, 3, 5, 7, 11]) == (
        [2] * 10 + [101]
    )


@given(st.integers(min_value=1, max_value=10**7))
def test_variants_agree_and_are_correct(n):
    result = trial_division(n)
    assert prod(result) == n
    assert all(is_prime(f) for f in result)
    assert result == sorted(result)
    assert trial_division_wheel(n) == result
    assert trial_division_primes(n) == result
