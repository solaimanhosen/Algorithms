"""Compare the three trial-division variants.

Run from the repository root:

    python benchmarks/trial_division.py

Two scenarios:

1. One hard number at a time (a product of two primes near √n). The sieve
   is rebuilt on every call, so the prime variant pays for it each time.
2. Many numbers sharing one prime table, built once up front.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from math import isqrt

from algorithms.factoring import (
    trial_division,
    trial_division_primes,
    trial_division_wheel,
)
from algorithms.primes import primes_up_to


def timed(fn: Callable[[], object]) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def single_hard_numbers() -> None:
    print("1. One hard number per call (semiprime p*q with p ≈ q)")
    print(f"   {'n':>22}  {'plain':>8}  {'wheel':>8}  {'primes':>8}")
    for p, q in [(10_007, 10_009), (100_003, 100_019), (1_000_003, 1_000_033)]:
        n = p * q
        times = [timed(lambda f=f, n=n: f(n)) for f in ALL]
        print(f"   {n:>22,}  " + "  ".join(f"{t:>7.3f}s" for t in times))


def many_numbers() -> None:
    rng = random.Random(0)
    count, top = 2000, 10**10
    numbers = [rng.randrange(2, top) for _ in range(count)]
    print(f"\n2. {count:,} random numbers below {top:,}")

    build = time.perf_counter()
    table = primes_up_to(isqrt(top))
    build = time.perf_counter() - build

    plain = timed(lambda: [trial_division(n) for n in numbers])
    wheel = timed(lambda: [trial_division_wheel(n) for n in numbers])
    fresh = timed(lambda: [trial_division_primes(n) for n in numbers])
    shared = timed(lambda: [trial_division_primes(n, primes=table) for n in numbers])
    print(f"   plain                        {plain:7.3f}s")
    print(f"   wheel                        {wheel:7.3f}s")
    print(f"   primes, new sieve per call   {fresh:7.3f}s")
    print(f"   primes, one shared table     {shared:7.3f}s (+ {build:.3f}s to build)")


ALL = [trial_division, trial_division_wheel, trial_division_primes]

if __name__ == "__main__":
    single_hard_numbers()
    many_numbers()
