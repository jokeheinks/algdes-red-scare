import pandas as pd
import subprocess
from glob import glob
from tqdm import tqdm


class color:
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


files = glob("data/*.txt")


scripts = {
    "none": "none.py",
    "some": "some.py",
    "many": "many.py",
    "few": "few.py",
    "alternate": "alternate.py",
}
out = []

for path in tqdm(files):
    with open(path, "r") as f:
        stdin = f.read()

    instance_name = path[path.index("/") + 1 : path.index(".")]
    n = int(stdin.split()[0])

    if n < 500:
        continue

    results = dict()
    for s in scripts:
        running = subprocess.run(
            ["python", scripts[s]], input=stdin.encode(), capture_output=True
        )
        res = running.stdout.decode("utf-8").strip()
        if res:
            results[s] = res
        else:
            results[s] = "?"
    # Format:   Instance name & $n$ & A & F & M & N & S \\
    out.append(
        f"{instance_name} & {n} & {results['alternate']} & {results['few']} & {results['many']} & {results['none']} & {results['some']} \\\\"
    )

with open("results_table.tex", "w") as f:
    f.write(r"""\begin{tabular}{lrrrrrr}
    \toprule
    Instance name & $n$ & A & F & M & N & S \\
    \midrule
    """)
    f.write("\n".join(sorted(out)))
    f.write(r"""  \bottomrule
\end{tabular}""")
