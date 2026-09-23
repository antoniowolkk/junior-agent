import importlib.util
import subprocess
import sys


def load_split_bill(repo_dir):
    spec = importlib.util.spec_from_file_location("billsplit", f"{repo_dir}/billsplit.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.split_bill


def grade(repo_dir):
    reasons = []

    existing = subprocess.run(
        ["python3", "test_billsplit.py"],
        cwd=repo_dir, capture_output=True, text=True,
    )
    if existing.returncode != 0:
        reasons.append("existing test suite no longer passes (regression): " + existing.stderr[-300:])

    try:
        split_bill = load_split_bill(repo_dir)
    except Exception as e:
        return False, [f"billsplit.py failed to import: {e}"]

    cases = [(1000, 3), (2000, 7), (999, 4), (10, 3), (100000, 13), (1, 5)]
    for amount, n in cases:
        try:
            shares = split_bill(amount, n)
        except Exception as e:
            reasons.append(f"split_bill({amount},{n}) raised {e}")
            continue
        if len(shares) != n:
            reasons.append(f"split_bill({amount},{n}) returned {len(shares)} shares, want {n}")
            continue
        if sum(shares) != amount:
            reasons.append(f"split_bill({amount},{n}) sums to {sum(shares)}, want {amount}")
        if max(shares) - min(shares) > 1:
            reasons.append(f"split_bill({amount},{n}) unfairly distributed: {shares}")

    try:
        split_bill(100, 0)
        reasons.append("split_bill(100, 0) should raise ValueError but did not")
    except ValueError:
        pass
    except Exception as e:
        reasons.append(f"split_bill(100, 0) raised {type(e).__name__}, want ValueError")

    return (len(reasons) == 0), reasons


if __name__ == "__main__":
    ok, reasons = grade(sys.argv[1])
    print("PASS" if ok else "FAIL")
    for r in reasons:
        print(" -", r)
    sys.exit(0 if ok else 1)
