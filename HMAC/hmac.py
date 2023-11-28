import sys
import hashlib

# Construct MAC using HMAC construction
def hmac(message, key, out):

    # Define the input and output pads for key padding
    ipad = b'\x36' * 64
    opad = b'\x5C' * 64

    # XOR the key with the input pad
    k_ipad = bytes([a ^ b for a, b in zip(read_file(key), ipad)])
    
    # XOR the key with the output pad
    k_opad = bytes([a ^ b for a, b in zip(read_file(key), opad)])
    
    # Compute the inner hash
    inner_hash = hashlib.sha256(k_ipad + read_file(message)).digest()
    
    # Compute the outer hash
    outer_hash = hashlib.sha256(k_opad + inner_hash).digest()

    return write_file(out, outer_hash)

#writes a sequence of bytes to a file
def write_file(output_file, byteseq):
    with open(output_file, "wb") as f:
        f.write(byteseq)

#reads a sequence of bytes from a file
def read_file(input_file):
    f = open(input_file, "rb")
    data = f.read()
    f.close()

    return data

def main():
    hmac(sys.argv[1], sys.argv[2], sys.argv[3])
    print("The MAC can be found in the file called:", sys.argv[3])
    
main()
