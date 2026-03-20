import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def parse_request_from_args() -> dict:
    parser = argparse.ArgumentParser(description="Send JSON request to Go via stdin/stdout.")
    parser.add_argument("--task", choices=["add", "mul", "pow"], help="Operation to perform")
    parser.add_argument("--a", type=float, help="First number")
    parser.add_argument("--b", type=float, help="Second number")
    parser.add_argument("--json", dest="json_str", help="Raw JSON request string")
    args = parser.parse_args()

    if args.json_str:
        return json.loads(args.json_str)

    # If task/a/b не переданы явно, пробуем читать входной JSON из stdin.
    if args.task is None and args.a is None and args.b is None:
        raw = sys.stdin.read()
        if not raw.strip():
            raise SystemExit("No input JSON provided via stdin and no --task/--a/--b given")
        return json.loads(raw)

    if args.task is None or args.a is None or args.b is None:
        raise SystemExit("--task/--a/--b must be provided together")

    return {"task": args.task, "a": args.a, "b": args.b}


def run_go(request: dict) -> str:
    here = Path(__file__).resolve()
    go_dir = (here.parent.parent / "go").resolve()

    req_json = json.dumps(request)
    proc = subprocess.run(
        ["go", "run", "."],
        cwd=str(go_dir),
        input=req_json.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # По условию контракт: Go всегда отвечает JSON в stdout.
    if proc.stderr:
        # stderr уводим в консоль разработчика, но stdout оставляем "чистым" JSON.
        sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))

    stdout_text = proc.stdout.decode("utf-8", errors="replace").strip()
    if stdout_text:
        return proc.stdout.decode("utf-8", errors="replace")

    # Если Go не смог запуститься/скомпилироваться, stdout может быть пустым.
    stderr_text = proc.stderr.decode("utf-8", errors="replace").strip()
    err_msg = stderr_text or f"go exited with code {proc.returncode}"
    return json.dumps({"error": err_msg})


def main() -> None:
    request = parse_request_from_args()
    response_json = run_go(request)
    sys.stdout.write(response_json)


if __name__ == "__main__":
    main()

