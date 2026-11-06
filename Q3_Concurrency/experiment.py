import os
import sys
import threading
import time
from fibonacci import fibonacci

NUMBERS = [35, 38, 40]     # the three Fibonacci inputs
ROUNDS = 10                # number of test rounds


def worker(n, index, records):
    """Thread task: calculate fibonacci(n) and record its own start/end time."""
    start = time.perf_counter_ns()
    result = fibonacci(n)
    end = time.perf_counter_ns()
    records[index] = (start, end, result)    # each thread writes to its OWN slot


def run_threaded():
    """One round with a separate thread per number.
    Returns (T in ns, list of results), where T = t2 - t1."""
    records = [None] * len(NUMBERS)
    threads = [threading.Thread(target=worker, args=(n, i, records))
               for i, n in enumerate(NUMBERS)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()                              # wait until all threads finish

    t1 = min(r[0] for r in records)           # start of the thread that started first
    t2 = max(r[1] for r in records)           # end of the thread that finished last
    return t2 - t1, [r[2] for r in records]


def run_sequential():
    """One round without threads. Returns (total time in ns, list of results)."""
    start = time.perf_counter_ns()
    results = [fibonacci(n) for n in NUMBERS]
    end = time.perf_counter_ns()
    return end - start, results


def run_experiment(title, func):
    """Run func for ROUNDS rounds, print each round, and return the average T."""
    print(f"\n=== Fibonacci Computation ({title}) ===")
    times = []
    for r in range(1, ROUNDS + 1):
        t, results = func()
        times.append(t)
        values = ", ".join(f"Fib({n})={v}" for n, v in zip(NUMBERS, results))
        print(f"Round {r:>2} : {values} | T = {t:,} ns")
    average = sum(times) // len(times)
    print(f"Average T ({title}) : {average:,} ns")
    return average


def main():
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]} | GIL enabled: {gil_enabled} "
          f"| CPU cores: {os.cpu_count()}")

    avg_threaded = run_experiment("With Multithreading", run_threaded)
    avg_sequential = run_experiment("Without Multithreading", run_sequential)

    change = (avg_sequential - avg_threaded) / avg_sequential * 100
    if change > 1:
        note = f"Multithreading reduced the average completion time by approximately {change:.1f}%."
    elif change < -1:
        note = f"Multithreading increased the average completion time by approximately {-change:.1f}%."
    else:
        note = f"Multithreading made no significant difference ({change:+.1f}%)."
    print(f"\nObservation: {note}")


if __name__ == "__main__":
    main()

