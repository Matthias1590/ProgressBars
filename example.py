from progressbars import ProgressBar, widgets

def isPrime(n: int) -> bool:
    "A very slow algorithm to calculate if a given number is prime."

    for i in range(2, n):
        if n % i == 0:
            return False
    return n > 1

# Create an empty list to store the primes we find
primes = []

# Create a red progress bar, update it every 10 iterations and use the percentage, iteration speed, counter, elapsed time and remaining time widgets
bar = ProgressBar([
    widgets.Percentage,
    widgets.IterationSpeed,
    widgets.Counter,
    widgets.ElapsedTime,
    widgets.RemainingTime
], 10, "red")

# Loop through all numbers from 0-30_000
for i in bar(range(30_000)):
    if isPrime(i): # If the current number is prime, append it to the primes list
        primes.append(i)

# Print how many primes we found
print("\nFound", len(primes), "primes!")