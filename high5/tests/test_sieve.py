import sys
import os
import pytest
import subprocess
import time
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'rust'))

from python.sieve import sieve_python

# Попытка загрузить Rust библиотеку через ctypes
RUST_AVAILABLE = False
try:
    from rust.ctypes_wrapper import sieve_rust
    RUST_AVAILABLE = True
except Exception as e:
    print(f"Rust library not available: {e}")

# Запуск Go сервиса, если не запущен
GO_AVAILABLE = False
GO_PROCESS = None

def start_go_service():
    """Запускает Go сервис в фоновом процессе."""
    global GO_PROCESS, GO_AVAILABLE
    if GO_AVAILABLE:
        return
    try:
        # Проверяем, уже ли запущен сервис
        resp = requests.get("http://localhost:5000/sieve", params={"limit": 10}, timeout=2)
        if resp.status_code == 200:
            GO_AVAILABLE = True
            return
    except:
        pass
    # Запускаем сервис
    go_dir = os.path.join(os.path.dirname(__file__), '..', 'go')
    exe_path = os.path.join(go_dir, 'sieve_go.exe')
    if not os.path.exists(exe_path):
        print("Go executable not found, skipping Go tests")
        return
    try:
        GO_PROCESS = subprocess.Popen([exe_path], cwd=go_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # Даём время на запуск
        GO_AVAILABLE = True
    except Exception as e:
        print(f"Failed to start Go service: {e}")

def stop_go_service():
    """Останавливает Go сервис."""
    global GO_PROCESS
    if GO_PROCESS:
        GO_PROCESS.terminate()
        GO_PROCESS.wait(timeout=5)
        GO_PROCESS = None

# Запускаем сервис перед всеми тестами
start_go_service()

# Регистрируем завершение сервиса после всех тестов
@pytest.fixture(scope="session", autouse=True)
def go_service_fixture():
    yield
    stop_go_service()

def test_sieve_python_basic():
    assert sieve_python(1) == []
    assert sieve_python(2) == [2]
    assert sieve_python(10) == [2, 3, 5, 7]
    assert sieve_python(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sieve_python_large():
    # Проверяем количество простых чисел до 1000 (известное значение)
    primes = sieve_python(1000)
    assert len(primes) == 168
    assert primes[0] == 2
    assert primes[-1] == 997

def test_sieve_python_edge():
    assert sieve_python(0) == []
    assert sieve_python(-5) == []

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust модуль не доступен")
def test_sieve_rust_basic():
    primes = sieve_rust(10)
    assert primes == [2, 3, 5, 7]
    primes = sieve_rust(30)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust модуль не доступен")
def test_sieve_rust_large():
    primes = sieve_rust(1000)
    assert len(primes) == 168
    assert primes[0] == 2
    assert primes[-1] == 997

@pytest.mark.skipif(not GO_AVAILABLE, reason="Go сервис не доступен")
def test_sieve_go_basic():
    resp = requests.get("http://localhost:5000/sieve", params={"limit": 10})
    assert resp.status_code == 200
    primes = resp.json()
    assert primes == [2, 3, 5, 7]

@pytest.mark.skipif(not GO_AVAILABLE, reason="Go сервис не доступен")
def test_sieve_go_large():
    resp = requests.get("http://localhost:5000/sieve", params={"limit": 1000})
    assert resp.status_code == 200
    primes = resp.json()
    assert len(primes) == 168
    assert primes[0] == 2
    assert primes[-1] == 997

if __name__ == "__main__":
    pytest.main([__file__])