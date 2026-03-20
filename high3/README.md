# Sieve of Eratosthenes – Rust + Python

High‑performance prime number generation using Rust with Python bindings.

## Features

- **Blazing fast**: Implemented in Rust with optimized Sieve of Eratosthenes.
- **Zero‑copy FFI**: Uses C‑compatible interfaces for minimal overhead.
- **Cross‑platform**: Works on Windows, macOS, and Linux.
- **Pythonic API**: Simple `sieve_primes(limit)` and `count_primes(limit)` functions.
- **Fully tested**: Unit tests for both Rust and Python layers.
- **CI/CD ready**: GitHub Actions for testing and PyPI deployment.

## Installation

### From PyPI (once published)

```bash
pip install sieve-rs
```

### From source

1. Ensure you have Rust and Python installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/example/sieve
   cd sieve
   ```
3. Build the Rust library:
   ```bash
   cd rust
   cargo build --release
   ```
4. Install the Python package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

```python
from sieve import sieve_primes, count_primes

# Get all primes up to 100
primes = sieve_primes(100)
print(primes)  # [2, 3, 5, 7, 11, ..., 97]

# Get only the count
n = count_primes(1_000_000)
print(f"There are {n} primes below one million.")
```

## Performance

Compared to a pure‑Python implementation, this library is **10–50× faster** depending on the limit.

## Development

### Project structure

```
high3/
├── rust/                 # Rust crate
│   ├── src/lib.rs       # Core implementation
│   └── Cargo.toml
├── python/              # Python wrapper
│   └── sieve.py
├── tests/               # pytest tests
│   └── test_sieve.py
├── .github/workflows/   # CI/CD pipelines
├── pyproject.toml       # Build configuration
└── README.md
```

### Running tests

```bash
cd high3
# Rust tests
cargo test --release
# Python tests
pytest tests/ -v
```

### Building wheels

With [maturin](https://www.maturin.rs):

```bash
maturin build --release
```

## CI/CD

The repository includes GitHub Actions that:

1. Run tests on Ubuntu, Windows, and macOS with multiple Python versions.
2. Build wheels for all supported platforms.
3. Automatically publish to PyPI when a tag is pushed.

## License

MIT – see [LICENSE](LICENSE) file.

## Contributing

Pull requests are welcome. Please ensure all tests pass and follow the code style.