"""Classical integer factoring algorithms."""

from algorithms.factoring.fermat import fermat_factor, fermat_factorize
from algorithms.factoring.trial_division import (
    trial_division,
    trial_division_primes,
    trial_division_wheel,
)

__all__ = [
    "fermat_factor",
    "fermat_factorize",
    "trial_division",
    "trial_division_primes",
    "trial_division_wheel",
]
