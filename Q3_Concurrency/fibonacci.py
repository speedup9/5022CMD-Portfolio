def fibonacci(n):
    """Return the nth Fibonacci number using recursion.

    fibonacci(0) = 0, fibonacci(1) = 1,
    fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)
    """
    if n <= 1:                                   # base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)   # two recursive calls


if __name__ == "__main__":
    for i in range(10):
        print(fibonacci(i), end=" ")             # 0 1 1 2 3 5 8 13 21 34
