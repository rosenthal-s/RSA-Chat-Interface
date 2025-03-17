import GeneratingLargePrimes as GenPrimes
import math
import random

if __name__ == '__main__':
    n = 1024
    # print( n, "-bit prime is:\n", GenPrimes.genPrime(n), sep="" )

    first_prime  = GenPrimes.genPrime(n)
    second_prime = GenPrimes.genPrime(n)
    # Very unlikely, but just want to make sure the two primes are different
    while first_prime == second_prime:
        second_prime = GenPrimes.genPrime(n)
    
    product_of_primes = first_prime * second_prime

    # Euler’s Totient function Φ(n) for an input n is the count of numbers in {1, 2, 3, …, n-1} that are relatively prime to n, i.e., the numbers whose GCD (Greatest Common Divisor) with n is 1.
    # If n is prime: Φ(n) = n-1 (because all numbers less than n are coprime to n)
    # If n is a power of a prime p^k: Φ(p^k) = p^k - p^(k-1)
    # If a and b are coprime, then Φ(a*b) = Φ(a) * Φ(b)
    eulers_totient = (first_prime-1) * (second_prime-1)

    encryption_exponent = random.randrange( 2, eulers_totient )
    while math.gcd( encryption_exponent, eulers_totient ) != 1:
        encryption_exponent = random.randrange( 2, eulers_totient )
    
    #test