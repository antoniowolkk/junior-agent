import importlib.util
import subprocess
import sys


def load_rate_limiter(repo_dir):
    spec = importlib.util.spec_from_file_location("rate_limiter", f"{repo_dir}/rate_limiter.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RateLimiter


def grade(repo_dir):
    reasons = []

    existing = subprocess.run(
        ["python3", "test_rate_limiter.py"],
        cwd=repo_dir, capture_output=True, text=True,
    )
    if existing.returncode != 0:
        reasons.append("existing test suite no longer passes (regression): " + existing.stderr[-300:])

    try:
        RateLimiter = load_rate_limiter(repo_dir)
    except Exception as e:
        return False, [f"rate_limiter.py failed to import: {e}"]

    # Core bug: the limiter must actually block once max_requests is hit
    # within the window, no matter how many times allow() is called at the
    # same or a nearby timestamp.
    rl = RateLimiter(max_requests=3, window_seconds=60)
    results = [rl.allow(0), rl.allow(0), rl.allow(0), rl.allow(0), rl.allow(0)]
    if results != [True, True, True, False, False]:
        reasons.append(f"burst at same timestamp: got {results}, want [T,T,T,F,F]")

    rl2 = RateLimiter(max_requests=2, window_seconds=60)
    results2 = [rl2.allow(0), rl2.allow(10), rl2.allow(20)]
    if results2 != [True, True, False]:
        reasons.append(f"burst spread across timestamps within window: got {results2}, want [T,T,F]")

    # Sliding window must actually expire old requests.
    rl3 = RateLimiter(max_requests=1, window_seconds=10)
    r1 = rl3.allow(0)
    r2 = rl3.allow(5)
    r3 = rl3.allow(25)
    if (r1, r2, r3) != (True, False, True):
        reasons.append(f"window expiry: got {(r1, r2, r3)}, want (True, False, True)")

    return (len(reasons) == 0), reasons


if __name__ == "__main__":
    ok, reasons = grade(sys.argv[1])
    print("PASS" if ok else "FAIL")
    for r in reasons:
        print(" -", r)
    sys.exit(0 if ok else 1)
