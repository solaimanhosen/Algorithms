# Algorithms

Python implementations of classic algorithms, each with tests.

## Factoring

Classical (non-quantum) integer factoring algorithms, listed from slowest to fastest. They'll be implemented in that order.

- [x] Fermat's method: `algorithms/factoring/fermat.py`
- [x] Trial division (plain, wheel, prime table): `algorithms/factoring/trial_division.py`
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

Create and activate a virtual environment:

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

On Windows, activate with `.venv\Scripts\activate` instead.

Install the package in editable mode with the test tools, then run the tests:

```bash
python -m pip install -e ".[dev]"
```

```bash
python -m pytest
```

Dependencies are declared in `pyproject.toml`; there is no `requirements.txt`.

Benchmarks live in `benchmarks/`, for example:

```bash
python benchmarks/trial_division.py
```
