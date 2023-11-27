### Overview

Implementation allowing one to encrypt and decrypt with block cipher inspired by the lightweight Simon cipher. It can handle files of any size by adding padding. Uses the following padding scheme which is a variant of PKCS#5 and PKCS#7 padding:

* Since the entire block is of size 16 bits, it can be seen as consisting of 2 bytes.
* Data from a file is read in sequences of bytes, so we should at most most need to pad by a single byte.
* If a single byte needs to be added to get a complete block, then we append a byte with value 1.
* If no padding is necessary, we append two bytes of value 16.

### penc

Reads input from a textfile, encrypts and gives the output as a textfile. 

### pdec

Reads input from a textfile, decrypts and gives the output as a textfile.