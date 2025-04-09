import GeneratingLargePrimes as GenPrimes
import math


# Greatest common denominator, using Basic Euclidean Algorithm
def gcdBasic(a, b):
    while b != 0:
        a, b = b, a % b
    return a


## Greatest common denominator, using Extended Euclidean Algorithm
## Taken from https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/ 
def gcdExtended(a, b, x, y):
    # Base Case
    if a == 0:
        x[0] = 0
        y[0] = 1
        return b

    # To store results of recursive call
    x1, y1 = [0], [0]
    gcd = gcdExtended(b % a, a, x1, y1)

    # Update x and y using results of recursive call
    x[0] = y1[0] - (b // a) * x1[0]
    y[0] = x1[0]

    return gcd


## Adapted from https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/ and https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
## a*x + b*y = gcd. # We want gcd to equal 1, so we can return x
def modInverse(a, b):
    x, y = [0], [1] # These are lists so they can be passed by reference

    gcd = gcdExtended(a, b, x, y)

    if (gcd != 1):
        raise Exception("Inverse doesn't exist")
    else:
        # b is added to handle negative x
        return (x[0] % b + b) % b


def stringToInt(s):
    return int.from_bytes(s.encode(), byteorder='little')


def intToString(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little').decode()


## Generate a pair of public and private keys for RSA encryption
def genKeys(num_bits):
    first_prime  = GenPrimes.genPrime(num_bits)
    second_prime = GenPrimes.genPrime(num_bits)
    # Very unlikely, but just want to make sure the two primes are different
    while first_prime == second_prime:
        second_prime = GenPrimes.genPrime(num_bits)

    product_of_primes = first_prime * second_prime

    # Euler’s Totient function Φ(n) for an input n is the count of numbers in {1, 2, 3, …, n-1} that are relatively prime to n,
    # i.e., the numbers whose GCD (Greatest Common Divisor) with n is 1.
    #
    # If n is prime: Φ(n) = n-1 (because all numbers less than n are coprime to n)
    # If n is a power of a prime p^k: Φ(p^k) = p^k - p^(k-1)
    # If a and b are coprime, then Φ(a*b) = Φ(a) * Φ(b)
    eulers_totient = (first_prime-1) * (second_prime-1)

    # Choose encryption exponent e, such that 1 < e < Φ(n) and e is co-prime with Φ(n)
    for encryption_exponent in range(2, eulers_totient):
        if gcdBasic(encryption_exponent, eulers_totient) == 1:
            break
    
    # Calculate decryption exponent d, such that: (d * e) % Φ(n) = 1.
    #
    # Using the Extended Euclidean Algorithm a.x + b.y = gcd. If a = e and b = Φ(n), we can say that gcd=1 since e is co-prime with Φ(n).
    # If we take modulo Φ(n) on both sides, we get e*x + Φ(n)*y ≡ 1 (mod Φ(n)). We can remove Φ(n)*y since mod Φ(n) will always be 0 for any y,
    # and so e*x ≡ 1 (mod Φ(n)) and therefore d = x.
    decryption_exponent = modInverse(encryption_exponent, eulers_totient)

    # print(f"First {numBits}-bit prime: {first_prime}")
    # print(f"\nSecond {numBits}-bit prime: {second_prime}")
    # print(f"\nProduct of primes: {product_of_primes}")
    # print(f"\nEuler's totient: {eulers_totient}")
    # print(f"\nEncryption exponent: {encryption_exponent}")
    # print(f"\nDecryption exponent: {decryption_exponent}\n\n")

    return encryption_exponent, decryption_exponent, product_of_primes


if __name__ == '__main__':
    encryption_exponent, decryption_exponent, product_of_primes = genKeys(1024)
    
    print(f"The public key (e, p): ({encryption_exponent}, {product_of_primes})")
    print(f"\nThe private key (d, p): ({decryption_exponent}, {product_of_primes})\n\n")

    # Provide a message, then convert the text to UTF-8
    message = input("Enter a message to encrypt\n")
    message_UTF = stringToInt(message)
    print("\nOriginal message:", intToString(message_UTF))
    print("Message in UTF-8:", message_UTF)

    # The message is encrypted by multiplying it to the power of the encryption exponent, modulo to the product of the primes
    encrypted_message_UTF = pow(message_UTF, encryption_exponent, product_of_primes)
    print("\nEncrypted message in UTF-8:", encrypted_message_UTF)
    # print("Encrypted message:", intToString(encrypted_message_UTF)) # It doesn't seem to like printing the encoded message - invalid characters, I suppose

    # decrypted_message = encrypted_message ** decryption_exponent % product_of_primes
    decrypted_message_UTF = pow(encrypted_message_UTF, decryption_exponent, product_of_primes)
    print("\nDecrypted message in UTF-8:", decrypted_message_UTF)
    print("Decrypted message:", intToString(decrypted_message_UTF))