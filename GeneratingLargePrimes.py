## Created using tutorial from https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/ and https://www.geeksforgeeks.org/sieve-of-eratosthenes/

#import math
import random



# The sieve of Eratosthenes is a method to find early prime numbers.
# This function returns a list of primes up to n.
def sieveOfEratosthenes( n ):
    # Create a boolean array "prime[0..n]" and initialize all entries as true.
    # A value in prime[i] will finally be false if i is not a prime, else it will remain true.
    sieve_table = [ True for i in range( n+1 ) ]
    p = 2
    while( p * p <= n ):
        # If primes[p] is not changed, then p is not one of its factors.
        # Once p^2 is larger than a given number, we know that it is prime.
        if( sieve_table[p] == True ):
            # Update all multiples of p
            for i in range( p*p, n+1, p ):
                sieve_table[i] = False
        p += 1

    first_primes_list = []
    for i in range( 2, n+1 ):
        if sieve_table[i]:
            first_primes_list.append( i )
        
    return first_primes_list



## Returns a random number between 2**(n-1)+1 and 2**n-1
#def nBitRandom( n ):
#    return random.randrange( 2**(n-1) + 1, 2**n - 1 )



## Returns a random odd number between 2**(n-1)+1 and 2**n-1
def nBitRandomOdd( n ):
    return random.randrange( 2**(n-1) + 1, 2**n, 2 )



## Generate a prime candidate divisible by first primes
def getLowLevelPrime( number_of_bits, first_primes_list ):
    # Repeat until a number satisfying the test isn't found
    while True:
        isPrime = True

        # Obtain a random odd number
#        candidate_prime = nBitRandom( number_of_bits )
        candidate_prime = nBitRandomOdd( number_of_bits ) ### Might as well force odd, right? I don't want the number 2 (if I change this, edit comment above)
#        print( candidate_prime ) ###

        for divisor in first_primes_list:
#            print( "Divisor = " + str( divisor ) + ", d^2 = " + str( divisor**2 ) + ", cp % d = " + str( candidate_prime % divisor ) ) ###
            # If the divisor squared is larger than the candidate prime, we do not need to keep searching
            if divisor**2 > candidate_prime: ### Could remove this section since it's only relevant for much smaller primes
                print("return") ###
                return candidate_prime
            # If a divisor is found, this candidate is not prime
            elif candidate_prime % divisor == 0:
#                print("break") ###
                isPrime = False
                break
        # If no divisor is found, return value
        if isPrime:
#            print("return v2") ###
            return candidate_prime



## Run 20 iterations of the Miller Rabin Primality Test.
## If we assume the test is correct 75% of the time, then
## chance of error becomes 0.25**20 = 9.094947e-13    ### This may be wrong
def isMillerRabinPassed( candidate_prime ):
    # Compute d and s such that d*(2**s) = n-1,
    # where d is an odd positive integer, the maximal odd divisor
    # and s is a positive integer
    max_odd_div = candidate_prime - 1
    s = 0
    while( max_odd_div % 2 == 0 ):
        max_odd_div //= 2
        s += 1
##    print("\n\nn - 1 = 2^", s, " * " , max_odd_div, " = ", max_odd_div*(2**s), sep="") ###

    # Test which returns False if the candidate prime passes one of the congruence relation tests
    def compositeTest():
        # An intenger a, called a base.
        ### Wikipedia claims it's supposed to be coprime to the candidate prime, but I can't find that anywhere else
        a = random.randint( 2, candidate_prime-1 ) ### Why did I have candidate_prime-2?
        if pow( a, max_odd_div, candidate_prime ) == 1:
            return False
        for i in range( s ):
            if pow( a, max_odd_div * 2**i, candidate_prime ) == candidate_prime - 1:
                return False
        return True
    
    # Do Miller-Rabin test 20 times.
    # If it is repeatedly
    for i in range( 0, 20 ):
        if compositeTest():
            return False
    return True



def genPrime( number_of_bits ):
    first_primes_list = sieveOfEratosthenes( 350 )

    while True:
        candidate_prime = getLowLevelPrime( number_of_bits, first_primes_list )

        if isMillerRabinPassed( candidate_prime ):
            return candidate_prime



if __name__ == '__main__':
#    n = 8 ###
    n = 1024
#     first_primes_list = sieveOfEratosthenes( 350 )
# ##    print( first_primes_list ) ###

#     while True:
#         candidate_prime = getLowLevelPrime( n, first_primes_list )
# ##        print( "candidate prime =", candidate_prime ) ###

#         if isMillerRabinPassed( candidate_prime ):
#             print( n, "-bit prime is:\n", candidate_prime, sep="" )
#             break   
    print( n, "-bit prime is:\n", genPrime(n), sep="" )