import pandas as pd
import subprocess


class color:
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


data = pd.read_csv("utils/test.csv")

scripts = {
    "none": "none.py",
    "some": "some.py",
    "many": "many.py",
    "few": "few.py",
    "alternate": "alternate.py",
}

for _, row in data.iterrows():
    with open(str(row["data"]), "rb") as f:
        stdin = f.read()

    print(f"Example {row['data']}")
    results = dict()
    for s in scripts:
        running = subprocess.run(
            ["python", scripts[s]], input=stdin, capture_output=True
        )
        res = running.stdout.decode("utf-8").strip()
        success = [
            color.ORANGE + "FAILED" + color.END,
            color.GREEN + "SUCCESS" + color.END,
        ]
        print(f"Script: {s} Status: {success[res == str(row[s])]}")
        if running.returncode != 0:
            print(f"{color.RED}Error{color.END} {running.stderr}")
    print()
