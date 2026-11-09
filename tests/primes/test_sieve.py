from math import isqrt

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algorithms.primes import iter_primes, primes_up_to


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


PRIMES_UNDER_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                    53, 59, 61, 67, 71, 73, 79, 83, 89, 97]  # fmt: skip


@pytest.mark.parametrize("sieve", [primes_up_to, lambda n: list(iter_primes(n))])
def test_primes_under_100(sieve):
    assert sieve(100) == PRIMES_UNDER_100


@pytest.mark.parametrize("sieve", [primes_up_to, lambda n: list(iter_primes(n))])
@pytest.mark.parametrize(
    ("limit", "expected"), [(0, []), (1, []), (2, [2]), (3, [2, 3]), (4, [2, 3])]
)
def test_small_limits(sieve, limit, expected):
    assert sieve(limit) == expected


@pytest.mark.parametrize(("limit", "count"), [(10**4, 1229), (10**5, 9592)])
def test_prime_counts(limit, count):
    # Known values of the prime-counting function pi(x).
    assert len(primes_up_to(limit)) == count
    assert sum(1 for _ in iter_primes(limit)) == count


@pytest.mark.parametrize("segment_size", [1, 2, 7, 64, 1000])
def test_segment_size_does_not_change_result(segment_size):
    assert list(iter_primes(5000, segment_size=segment_size)) == primes_up_to(5000)


def test_iter_primes_is_lazy():
    # Asking for the first few primes below 10**12 must not sieve the whole range.
    gen = iter_primes(10**12)
    assert [next(gen) for _ in range(5)] == [2, 3, 5, 7, 11]


@pytest.mark.parametrize("bad", [-1, -100])
def test_rejects_negative_limit(bad):
    with pytest.raises(ValueError):
        primes_up_to(bad)
    with pytest.raises(ValueError):
        list(iter_primes(bad))


@pytest.mark.parametrize("bad", [10.0, "10", None, True])
def test_rejects_non_int_limit(bad):
    with pytest.raises(TypeError):
        primes_up_to(bad)
    with pytest.raises(TypeError):
        list(iter_primes(bad))


def test_rejects_bad_segment_size():
    with pytest.raises(ValueError):
        list(iter_primes(100, segment_size=0))
    with pytest.raises(ValueError):
        list(iter_primes(100, segment_size=-5))


@given(st.integers(min_value=0, max_value=3000))
def test_matches_reference(limit):
    expected = [k for k in range(limit + 1) if is_prime(k)]
    assert primes_up_to(limit) == expected
    assert list(iter_primes(limit, segment_size=37)) == expected
