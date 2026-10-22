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
    """Run one round with 3 threads. Returns T = t2 - t1 in nanoseconds."""
    records = [None] * len(NUMBERS)
    threads = [threading.Thread(target=worker, args=(n, i, records))
               for i, n in enumerate(NUMBERS)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()                              # wait until all threads finish

    t1 = min(r[0] for r in records)           # start of the thread that started first
    t2 = max(r[1] for r in records)           # end of the thread that finished last
    return t2 - t1


def run_sequential():
    """Run one round without threads. Returns the total time in nanoseconds."""
    start = time.perf_counter_ns()
    for n in NUMBERS:
        fibonacci(n)
    end = time.perf_counter_ns()
    return end - start


def run_experiment(title, func):
    """Run func for ROUNDS rounds, print each time, return the average."""
    print(f"\n===== {title} =====")
    times = []
    for r in range(1, ROUNDS + 1):
        t = func()
        times.append(t)
        print(f"Round {r:>2}: {t:>18,} ns")
    average = sum(times) // len(times)
    print("-" * 32)
    print(f"Average : {average:>18,} ns")
    return average


def main():
    print(f"Calculating Fibonacci{tuple(NUMBERS)} | {ROUNDS} rounds each")
    avg_threaded = run_experiment("With multithreading", run_threaded)
    avg_sequential = run_experiment("Without multithreading", run_sequential)

    print("\n===== Comparison =====")
    print(f"Threaded average   : {avg_threaded:>18,} ns")
    print(f"Sequential average : {avg_sequential:>18,} ns")
    print(f"Threaded / Sequential ratio: {avg_threaded / avg_sequential:.2f}")


if __name__ == "__main__":
    main()
