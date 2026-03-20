import json
import sys
from io import StringIO

from pathlib import Path

HERE = Path(__file__).resolve()
PY_DIR = HERE.parents[2] / "python"
sys.path.insert(0, str(PY_DIR))

import main as py_main  # noqa: E402


def test_parse_request_from_args_stdin(monkeypatch):
    test_input = {"task": "add", "a": 2, "b": 3}
    stdin = StringIO(json.dumps(test_input))

    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "argv", ["main.py"])

    req = py_main.parse_request_from_args()
    assert req == test_input


def test_parse_request_from_args_explicit(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "--task", "mul", "--a", "4", "--b", "5"])
    req = py_main.parse_request_from_args()
    assert req == {"task": "mul", "a": 4.0, "b": 5.0}


def test_run_go_returns_json_stdout(monkeypatch):
    class MockProc:
        stdout = b'{"result": 5}'
        stderr = b""
        returncode = 0

    def mock_run(*args, **kwargs):
        return MockProc()

    monkeypatch.setattr(py_main.subprocess, "run", mock_run)

    resp = py_main.run_go({"task": "add", "a": 2, "b": 3})
    assert resp == '{"result": 5}'


def test_run_go_when_stdout_empty_returns_error_json(monkeypatch):
    class MockProc:
        stdout = b""
        stderr = b"some go error"
        returncode = 1

    def mock_run(*args, **kwargs):
        return MockProc()

    monkeypatch.setattr(py_main.subprocess, "run", mock_run)

    resp = py_main.run_go({"task": "add", "a": 2, "b": 3})
    decoded = json.loads(resp)
    assert "error" in decoded
    assert decoded["error"]

