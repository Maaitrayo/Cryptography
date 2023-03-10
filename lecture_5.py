# Using insecure AES-ECB in python link: https://youtu.be/-0e-LzrxrfQ

import os
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB
from cryptography.hazmat.primitives import padding 

if __name__ == "__main__":
    # Plain text to be kept confidential
    plaintext = b'Fundamental Cryptography in Python'
    print(f"Plaintext: {plaintext}")

    # 256-bit AES Key
    ''' 256 bits = 256 bytes // 8
        As os.urandom samples bytes
    '''
    key = os.urandom(256 // 8)
    # print(key)

    # Create AES ECB cipher
    aes_ecb_cipher = Cipher(AES(key), ECB())

    # Encrypt 
    ciphertext = aes_ecb_cipher.encryptor().update(plaintext)
    print(f"Ciphertext: {ciphertext} ")

    # Decrypt
    '''
        will not recover the original plaintext as it needs to be a multiple of 128 bits
        "Fundamental Cryptography in Python" --> 34 bytes
        34 bytes = 2*128 bits + 16 bits
        8 bits = 1 byte
        '''
    recoverd_plaintext = aes_ecb_cipher.decryptor().update(ciphertext)
    print(f"Recovered plaintext: {recoverd_plaintext}")

    # Pad the plaintext
    aes_block_size_in_bits = 128
    pkcs7_padder = padding.PKCS7(aes_block_size_in_bits).padder()
    padded_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize()
    print(f"Padded plaintext: {padded_plaintext}")

    # Encrypt with padding
    ciphertext = aes_ecb_cipher.encryptor().update(padded_plaintext)
    print(f"Ciphertext: {ciphertext}")

    # Decrypt with padding
    recovered_plaintext_with_padding = aes_ecb_cipher.decryptor().update(ciphertext)
    print(f"Recovered plaintext + padding: {recovered_plaintext_with_padding}")

    # Remove padding from plaintext
    pkcs7_unpadder = padding.PKCS7(aes_block_size_in_bits).unpadder()
    recovered_plaintext = pkcs7_unpadder.update(recovered_plaintext_with_padding) + pkcs7_unpadder.finalize()
    print(f"Recovered plaintext: {recovered_plaintext}")
    assert (plaintext == recovered_plaintext)

    # Encrypt mandlebrot.ppm

    # Read the image into memory
    with open("RESOURSES/mandelbrot.ppm", "rb") as image:
        image_file = image.read()
        image_bytes = bytearray(image_file)

    # keep ppm header
    header_size = 17 # previously checked
    image_header = image_bytes[:header_size]
    image_body = image_bytes[header_size:]

    # pad the image body
    pkcs7_padder = padding.PKCS7(aes_block_size_in_bits).padder()
    padded_image_body = pkcs7_padder.update(image_body) + pkcs7_padder.finalize()

    # Encrypt the image body
    encrypted_image_body = aes_ecb_cipher.encryptor().update(padded_image_body)

    # Assemble encrypted image
    encrypted_image = image_header + encrypted_image_body[:len(image_body)]

    # Create and save the full encrypted image
    with open("OUTPUT/mandelbrot_aes_ecb_encrypted.ppm", "wb") as image_encrypted:
        image_encrypted.write(encrypted_image)


