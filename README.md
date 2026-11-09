# Algorithms

Python implementations of classic algorithms, each with tests.

## Factoring

Classical (non-quantum) integer factoring algorithms, listed from slowest to fastest. They'll be implemented in that order.

- [x] Fermat's method: `algorithms/factoring/fermat.py`
- [ ] Trial division
- [ ] Lehman's method
- [ ] Pollard's p − 1
- [ ] Williams' p + 1
- [ ] Pollard's rho (Floyd and Brent cycle detection)
- [ ] Shanks' square forms (SQUFOF)
- [ ] Dixon's random squares
- [ ] Continued fraction (CFRAC)
- [ ] Lenstra elliptic curve method (ECM)
- [ ] Quadratic sieve (QS / MPQS / SIQS)
- [ ] General number field sieve (GNFS)

## Development

Requires Python 3.10+.

```bash
python -m pip install -e ".[dev]"
python -m pytest
```
