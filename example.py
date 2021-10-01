from progressbars import ProgressBar

def isPrime(n: int) -> bool:
    "A very slow algorithm to calculate if a given number is prime."

    for i in range(2, n):
        if n % i == 0:
            return False
    return n > 1

# Create an empty list to store the primes we find
primes = []

# Loop through all numbers from 0-100_000
for i in ProgressBar(range(100_000), 30): # Update the progress bar every 30 iterations
    if isPrime(i): # If the current number is prime, append it to the primes list
        primes.append(i)

# Print how many primes we found
print("\nFound", len(primes), "primes!")