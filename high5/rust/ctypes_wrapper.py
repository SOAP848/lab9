import ctypes
import os
import sys

def load_rust_lib():
    """Загружает Rust библиотеку и возвращает объект с функциями."""
    # Определяем путь к библиотеке в зависимости от ОС
    if sys.platform == "win32":
        lib_name = "sieve_rust.dll"
    elif sys.platform == "darwin":
        lib_name = "libsieve_rust.dylib"
    else:
        lib_name = "libsieve_rust.so"
    lib_path = os.path.join(os.path.dirname(__file__), "target", "release", lib_name)
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"Rust library not found at {lib_path}")
    lib = ctypes.CDLL(lib_path)
    # Определяем сигнатуры функций
    lib.sieve_rust.argtypes = [ctypes.c_uint]
    lib.sieve_rust.restype = ctypes.POINTER(ctypes.c_uint)
    lib.free_sieve_result.argtypes = [ctypes.POINTER(ctypes.c_uint)]
    lib.free_sieve_result.restype = None
    return lib

def sieve_rust(limit):
    """Вызывает Rust реализацию решета Эратосфена."""
    lib = load_rust_lib()
    ptr = lib.sieve_rust(limit)
    if ptr is None:
        return []
    # Собираем числа, пока не встретим 0 (маркер конца)
    result = []
    i = 0
    while ptr[i] != 0:
        result.append(ptr[i])
        i += 1
    lib.free_sieve_result(ptr)
    return result

if __name__ == "__main__":
    # Пример использования
    primes = sieve_rust(30)
    print(primes)