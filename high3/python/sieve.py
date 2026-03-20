"""
Python wrapper for the Rust Sieve of Eratosthenes library.
Uses ctypes to call the compiled shared library.
"""
import ctypes
import os
import sys
from typing import List, Optional

# Determine library extension based on platform
if sys.platform == "win32":
    lib_name = "sieve.dll"
elif sys.platform == "darwin":
    lib_name = "libsieve.dylib"
else:
    lib_name = "libsieve.so"

# Try to locate the library
# In development, we assume it's in ../rust/target/debug/ or ../rust/target/release/
def find_library() -> Optional[str]:
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "rust", "target", "debug", lib_name),
        os.path.join(os.path.dirname(__file__), "..", "rust", "target", "release", lib_name),
        os.path.join(os.path.dirname(__file__), lib_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

lib_path = find_library()
if lib_path is None:
    raise RuntimeError(
        f"Rust library '{lib_name}' not found. Please build it with 'cargo build --release'."
    )

lib = ctypes.CDLL(lib_path)

# Define function signatures
lib.sieve_primes.argtypes = [
    ctypes.c_int,          # limit
    ctypes.POINTER(ctypes.c_int),  # out buffer
    ctypes.c_int,          # out_len
]
lib.sieve_primes.restype = ctypes.c_int

lib.count_primes.argtypes = [ctypes.c_int]
lib.count_primes.restype = ctypes.c_int


def sieve_primes(limit: int) -> List[int]:
    """
    Return a list of prime numbers up to `limit` (inclusive).
    """
    if limit < 0:
        raise ValueError("limit must be non‑negative")
    count = lib.count_primes(limit)
    if count < 0:
        raise RuntimeError("Internal error in count_primes")
    if count == 0:
        return []
    # Allocate buffer for the primes
    buffer = (ctypes.c_int * count)()
    result = lib.sieve_primes(limit, buffer, count)
    if result != count:
        raise RuntimeError(
            f"Buffer size mismatch: expected {count}, got {result}"
        )
    return list(buffer)


def count_primes(limit: int) -> int:
    """
    Return the number of primes up to `limit` (inclusive).
    """
    if limit < 0:
        raise ValueError("limit must be non‑negative")
    result = lib.count_primes(limit)
    if result < 0:
        raise RuntimeError("Internal error in count_primes")
    return result


if __name__ == "__main__":
    # Simple demo
    import argparse
    parser = argparse.ArgumentParser(description="Sieve of Eratosthenes demo")
    parser.add_argument("limit", type=int, help="Upper limit")
    args = parser.parse_args()
    primes = sieve_primes(args.limit)
    print(f"Primes up to {args.limit}: {primes}")
    print(f"Count: {len(primes)}")