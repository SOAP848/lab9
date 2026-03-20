import sys
import threading
from io import StringIO
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
PY_DIR = HERE.parents[2] / "python"
sys.path.insert(0, str(PY_DIR))

import main as py_main  # noqa: E402


def test_parse_request_from_args_stdin(monkeypatch):
    stdin = StringIO("add 2 3")

    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "argv", ["main.py"])

    req = py_main.parse_request_from_args()
    assert req == {"task": "add", "a": 2.0, "b": 3.0}


def test_parse_request_from_args_explicit(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "--task", "mul", "--a", "4", "--b", "5"])
    req = py_main.parse_request_from_args()
    assert req == {"task": "mul", "a": 4.0, "b": 5.0}


def test_run_go_returns_json_stdout(monkeypatch):
    class MockProc:
        stdout = b"5\n"
        stderr = b""
        returncode = 0

    def mock_run(*args, **kwargs):
        return MockProc()

    monkeypatch.setattr(py_main.subprocess, "run", mock_run)

    resp = py_main.run_go({"task": "add", "a": 2, "b": 3})
    assert resp == "5"


def test_run_go_when_stdout_empty_returns_error_text(monkeypatch):
    class MockProc:
        stdout = b""
        stderr = b"some go debug"
        returncode = 1

    def mock_run(*args, **kwargs):
        return MockProc()

    monkeypatch.setattr(py_main.subprocess, "run", mock_run)

    resp = py_main.run_go({"task": "add", "a": 2, "b": 3})
    assert resp.startswith("ERROR go exited with code")


def test_run_go_background_executes_in_thread(monkeypatch):
    started = threading.Event()

    def mock_run_go(_request: dict) -> str:
        started.set()
        return "OK"

    monkeypatch.setattr(py_main, "run_go", mock_run_go)

    resp = py_main.run_go_background({"task": "add", "a": 2, "b": 3})
    assert started.is_set()
    assert resp == "OK"


def test_run_go_background_returns_error_json_on_exception(monkeypatch):
    def mock_run_go(_request: dict) -> str:
        raise ValueError("boom")

    monkeypatch.setattr(py_main, "run_go", mock_run_go)

    resp = py_main.run_go_background({"task": "add", "a": 2, "b": 3})
    assert resp.startswith("ERROR")

