import sys

# Performs encryption on all 16 bit blocks of the plaintext
def enc(plaintext, key, iv, output_file):
    xor = bytes_to_bits(read_file(iv))
    ciphertext = []
    padded_plaintext = add_padding(read_file(plaintext)) # Add padding to plaintext
    for block in divide_16_bit_blocks(bytes_to_bits(padded_plaintext)):
        xor_block = []
        for bit in range(16):
            xor_block.append(block[bit] ^ xor[bit])
        cipher_block = simon_encrypt(xor_block, bytes_to_bits(read_file(key)))
        xor = cipher_block
        ciphertext.extend(cipher_block)
    return write_file(output_file, bits_to_bytes(ciphertext))

# Adds padding
def add_padding(data):
    byte_count = len(data)
    if byte_count % 2 == 1:
        # Byte number is odd (not divisible by 16), append one byte padding
        data += b'\x01'
    else:
        # Byte number is even (divisible by 16), append two bytes padding
        data += b'\x10\x10'
    return data

# Divides the list of bits plaintext into list of lists where each list contains 16 bits
def divide_16_bit_blocks(bits):
    return [bits[i:i+16] for i in range(0, len(bits), 16)]

# Performs a left cyclic shift by k bits.
# From mandatory assignment 1 problem 3
def circular_shift_left(bits, k):
    return bits[k:] + bits[:k]

# Performs four rounds of encryption
# From mandatory assignment 1 problem 3
def simon_encrypt(block, key):
    # Separate the plaintext block into two blocks.
    left_half = block[:8]
    right_half = block[8:]

    # Gets the list of roundkeys
    keys = round_keys(key)

    # Performs the four rounds of the Simon cipher
    for i in range(0, 4):
        left_half, right_half = one_encryption_round(left_half, right_half, keys, i)

    # Concatenate the left and right halves to form the ciphertext
    ciphertext = right_half + left_half

    return ciphertext

# One round of the simon cipher encryption
# From mandatory assignment 1 problem 3
def one_encryption_round(left, right, round_key, round):
    new_right = left
    new_left = []
    for i in range(8):
        new_left.append(((circular_shift_left(left, 1)[i] & circular_shift_left(left, 5)[i]) ^ right[i] ^ circular_shift_left(left, 2)[i] ^ round_key[round][i]))
    return new_left, new_right

# Generates the roundkeys by taking the 32 bit key as input and returning a list of lists with the four roundkeys.
# From mandatory assignment 1 problem 3
def round_keys(key):
    list_of_roundkeys = []
    for i in range(0, 32, 8):
        list_of_roundkeys.append(key[i:i+8])
    return list_of_roundkeys

# Converts a sequence of bytes (read from a file) into a list of bits (0s and 1s)
# Taken from cipher.py
def bytes_to_bits(B):
    bits = []
    for i in range(len(B)):
        current_byte = B[i]
        mask = 128
        for j in range(8):
            if (current_byte >= mask):
                bits.append(1)
                current_byte -= mask
            else:
                bits.append(0)
            mask = mask // 2
    return bits

# Converts a list of bits to a sequence of bytes
# Taken from cipher.py
def bits_to_bytes(B):
    byteseq = []
    num_bytes = len(B) // 8
    assert 8*num_bytes == len(B)
    for i in range(num_bytes):
        current_byte = 0
        bit_sequence = B[(i*8):((i+1)*8)]
        mask = 128
        for j in range(8):
            current_byte += mask * bit_sequence[j]
            mask = mask // 2
        byteseq.append(current_byte.to_bytes(1,"big"))
    return byteseq

# reads a sequence of bytes from a file
# Taken from cipher.py
def read_file(input_file):
    f = open(input_file, "rb")
    data = f.read()
    f.close()

    return data

# writes a sequence of bytes to a file
# Taken from cipher.py
def write_file(output_file, byteseq):
    f = open(output_file, "wb")
    for i in range(len(byteseq)):
        f.write(byteseq[i])
    f.close()

# Main method used to take in arguments from terminal and return the result in a text file
def main():
    enc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print("The result of the encryption can be found in the file called:", sys.argv[4])
main()