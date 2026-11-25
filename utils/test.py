import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path

import pandas as pd


class Color:
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


TIMEOUT_SECONDS = 10  # Raise this (e.g. 3600) for large benchmark runs


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for stream in self.streams:
            stream.write(text)
        return len(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def run_tests():
    data = pd.read_csv("utils/test.csv", dtype=str, keep_default_na=False)
    data.columns = data.columns.str.strip()

    scripts = {
        "none": "none.py",
        "some": "some.py",
        "many": "many.py",
        "few": "few.py",
        "alternate": "alternate.py",
    }

    for _, row in data.iterrows():
        raw_path = row["data"].strip()
        data_path = Path(raw_path)
        print(f"Example: {raw_path}")

        if not raw_path or not data_path.is_file():
            print(
                f"  {Color.RED}ERROR{Color.END} "
                f"Data file not found: {raw_path!r}\n"
            )
            continue

        try:
            stdin = data_path.read_bytes()
        except OSError as e:
            print(f"  {Color.RED}ERROR{Color.END} Could not read {raw_path!r}: {e}\n")
            continue

        for name, script_path in scripts.items():
            if name not in data.columns:
                print(
                    f"  Script: {name:<10} Status: "
                    f"{Color.ORANGE}SKIPPED (missing '{name}' column in CSV){Color.END}"
                )
                continue

            if not Path(script_path).is_file():
                print(
                    f"  Script: {name:<10} Status: "
                    f"{Color.ORANGE}MISSING ({script_path}){Color.END}"
                )
                continue

            expected = row[name].strip()

            try:
                running = subprocess.run(
                    [sys.executable, script_path],
                    input=stdin,
                    capture_output=True,
                    timeout=TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired:
                print(
                    f"  Script: {name:<10} Status: "
                    f"{Color.RED}TIMEOUT (>{TIMEOUT_SECONDS}s){Color.END}"
                )
                continue

            res = running.stdout.decode("utf-8", errors="replace").strip()
            err = running.stderr.decode("utf-8", errors="replace").strip()

            if running.returncode != 0:
                print(
                    f"  Script: {name:<10} Status: "
                    f"{Color.RED}CRASHED (exit {running.returncode}){Color.END}"
                )
                if err:
                    print(f"    {Color.RED}Stderr:{Color.END} {err}")
            elif res == expected:
                print(f"  Script: {name:<10} Status: {Color.GREEN}SUCCESS{Color.END}")
            else:
                print(
                    f"  Script: {name:<10} Status: {Color.ORANGE}FAILED{Color.END} "
                    f"(expected: {expected!r}, got: {res!r})"
                )
                if err:
                    print(f"    {Color.ORANGE}Stderr:{Color.END} {err}")

        print()


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    timestamp = datetime.now().strftime("%Y-%m-%d, %H-%M-%S-%f")
    report_path = repo_root / f"test_run[{timestamp}].txt"

    with report_path.open("w", encoding="utf-8") as report:
        stdout_tee = Tee(sys.stdout, report)
        stderr_tee = Tee(sys.stderr, report)
        with redirect_stdout(stdout_tee), redirect_stderr(stderr_tee):
            run_tests()
            print(f"Full test output saved to {report_path}")
