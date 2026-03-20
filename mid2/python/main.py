import argparse
import subprocess
import sys
import threading
from pathlib import Path
from queue import Queue


def parse_request_from_args() -> dict:
    parser = argparse.ArgumentParser(description="Send text request to Go via stdin/stdout.")
    parser.add_argument("--task", choices=["add", "mul", "pow"], help="Operation to perform")
    parser.add_argument("--a", type=float, help="First number")
    parser.add_argument("--b", type=float, help="Second number")
    args = parser.parse_args()

    # If task/a/b not passed explicitly, try reading text from stdin:
    #   "<task> <a> <b>"
    if args.task is None and args.a is None and args.b is None:
        raw = sys.stdin.read()
        raw = raw.strip()
        if not raw:
            raise SystemExit("No input provided via stdin and no --task/--a/--b given")
        parts = raw.split()
        if len(parts) < 3:
            raise SystemExit("stdin must be: <task> <a> <b>")
        task = parts[0]
        if task not in {"add", "mul", "pow"}:
            raise SystemExit(f"unknown task: {task}")
        a = float(parts[1])
        b = float(parts[2])
        return {"task": task, "a": a, "b": b}

    if args.task is None or args.a is None or args.b is None:
        raise SystemExit("--task/--a/--b must be provided together")

    return {"task": args.task, "a": args.a, "b": args.b}


def run_go(request: dict) -> str:
    here = Path(__file__).resolve()
    go_dir = (here.parent.parent / "go").resolve()

    # Contract (no JSON): "<task> <a> <b>\n"
    req_text = f"{request['task']} {request['a']} {request['b']}\n"
    proc = subprocess.run(
        ["go", "run", "."],
        cwd=str(go_dir),
        input=req_text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.stderr:
        sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))

    stdout_text = proc.stdout.decode("utf-8", errors="replace").strip()
    if stdout_text:
        return stdout_text

    return f"ERROR go exited with code {proc.returncode}"


def run_go_background(request: dict) -> str:
    """
    Запускаем обработку запроса в фоне (Python Thread),
    чтобы соответствовать идее "фоновой обработки" запросов,
    реализованной в Go через горутину.
    """

    q: Queue[str] = Queue(maxsize=1)

    def worker() -> None:
        try:
            q.put(run_go(request))
        except Exception as exc:  # pragma: no cover (defensive)
            q.put(f"ERROR {str(exc)}")

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    result = q.get()  # wait background thread
    t.join(timeout=1)
    return result


def main() -> None:
    request = parse_request_from_args()
    response_text = run_go_background(request)
    sys.stdout.write(response_text)


if __name__ == "__main__":
    main()

