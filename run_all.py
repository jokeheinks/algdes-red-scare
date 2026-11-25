"""Run all five solutions on every instance in data/ and write results.txt.

Format (see doc/report.tex): tab-separated columns
    Instance name, n, A, F, M, N, S
for Alternate, Few, Many, None and Some. Booleans are written as true/false.
'?!' means the instance is outside the graph class our polynomial-time
algorithm handles, because the problem is NP-hard in general.

Also writes timings.txt with the running time (seconds) of each solution.

Usage (from the repository root): python run_all.py
"""
import glob
import os
import subprocess
import sys
import time

PROBLEMS = [("A", "alternate.py"), ("F", "few.py"), ("M", "many.py"),
            ("N", "none.py"), ("S", "some.py")]


def fmt(out):
    out = out.strip()
    if out == "?":
        return "?!"
    return {"True": "true", "False": "false"}.get(out, out)


def main():
    files = sorted(glob.glob("data/*.txt"))
    with open("results.txt", "w") as res, open("timings.txt", "w") as tim:
        res.write("\t".join(["Instance name", "n"] + [p for p, _ in PROBLEMS]) + "\n")
        tim.write("\t".join(["Instance name", "n"] + [p for p, _ in PROBLEMS]) + "\n")
        for f in files:
            name = os.path.splitext(os.path.basename(f))[0]
            with open(f, "rb") as fh:
                data = fh.read()
            n = data.split(maxsplit=1)[0].decode()
            answers, times = [], []
            for _, script in PROBLEMS:
                start = time.perf_counter()
                run = subprocess.run([sys.executable, script], input=data,
                                     capture_output=True)
                times.append(f"{time.perf_counter() - start:.2f}")
                if run.returncode != 0:
                    print(f"{script} crashed on {name}:\n{run.stderr.decode()}",
                          file=sys.stderr)
                    answers.append("?")
                else:
                    answers.append(fmt(run.stdout.decode()))
            res.write("\t".join([name, n] + answers) + "\n")
            tim.write("\t".join([name, n] + times) + "\n")
            res.flush()
            tim.flush()
            print(name, n, *answers, flush=True)


if __name__ == "__main__":
    main()
