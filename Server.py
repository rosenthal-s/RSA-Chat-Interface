import socket
import RSA

def connectToClient():
    # Create a socket at server-side using TCP/IP protocol
    s = socket.socket()
    print ("Socket successfully created")
    
    # Bind the socket with server and port numbers
    port = 5000
    s.bind(('', port))
    print ("Socket bound to %s" %(port)) 
    
    # Allow a maximum of 1 connection to the socket
    s.listen(1)
    
    # Wait until a client accept the connection
    c, addr = s.accept()
    
    # Display client address
    print("CONNECTION FROM:", str(addr))

    return c

if __name__ == '__main__':
    c = connectToClient()

    # Generate the necessary values for the public and private key using the RSA program
    encryption_exponent, decryption_exponent, product_of_primes = RSA.genKeys(1024)

    # Send the public key to the client, so they can encrypt their messages
    print("Public key to send: (", encryption_exponent, " ,", product_of_primes, ")", sep="" )
    c.send(bytes([encryption_exponent]))
    c.send(product_of_primes.to_bytes(256))

    # Begin receiving messages from the client
    message = "\n\nReceiving messages now\n"
    # Repeat as long as message string is not empty
    while message:
        print(message)
        encrypted_message = int.from_bytes(c.recv(1024))
        print("\nEncrypted message:", encrypted_message)
        message = RSA.intToString(pow(encrypted_message, decryption_exponent, product_of_primes))

    # disconnect the server
    c.close()