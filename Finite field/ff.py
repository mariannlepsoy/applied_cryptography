# To run the problem you just press run and it will create the lookup table as a text file called "lookup_table.txt"

# Generate the lookup table for the function F(x, k)
def generate_lookup_table():
    with open('lookup_table.txt', 'w') as file:
        for i in range(2**6): # Get all possible x values
            x_str = format(i, '06b') # Turn the integer into a string
            x = string_to_bits(x_str) # Turn the string into a list of bits
            for j in range(2**6): # Get all possible k values
                k_str = format(j, '06b') # Turn the integer into a string
                k = string_to_bits(k_str) # Turn the string into a list of bits
                f = F(x, k) # Get the result of function F for the current x and k values
                file.write(f'{bits_to_string(x)},{bits_to_string(k)}->{bits_to_string(f)}\n') # Writes the lookup table into the text file

# Finite field addition
def addition(x, k):
    added = []
    # Goes through all the bits in the lists and XOR them
    for i in range(6):
        added.append(x[i] ^ k[i])
    return added

# Finite field multiplication
def multiply(x, k):
    p = [1, 1, 0, 0, 0, 0] # The primitive polynomial x^6 = x + 1
    o = [0, 0, 0, 0, 0, 0] # The output result
    overflow = 7 # The number that is overflow

    # Loop to go through each of the bits in the list
    for i in range(6):
        # If the bit at position i is 0, it skipps it
        if k[i] == 0:
            continue
        
        # If the bit at position i is 1
        else:
            n = 0
            shifted = x.copy() # Saves a copy of x that is updated for each loop of the while-loop.
            while n < i: # Runs i times
                shifted_x = shift(shifted) # Shift the bits one position to the right.
                if len(shifted_x) == overflow: # Checks if the list is longer than 6 bits
                    valid_bits = shifted_x[:6] # Keep the valid first 6 bits
                    for j in range(6):
                        valid_bits[j] ^= p[j] # XOR the valid bits with the primitive polynomial
                    shifted = valid_bits # Update the saved copy of x to the shifted version
                else:
                    shifted = shifted_x # Update the saved copy of x to the shifted version
                n += 1 
            for l in range(6):
                o[l] ^= shifted[l] # Update the result

    return o

# Shifts all the bits in the list to the right by one position
def shift(x):
    x_copy = x.copy() # Create copy of x so the x value is not changed
    if x_copy[-1] == 0: # If the last bit is 0, it just shifts everything to the right and keeps the length of the list
        x_copy.insert(0, 0)
        x_copy = x_copy[:-1]
    else: # If the last bit is 1, it shifts all the bits to the right and increases the size of the list by one, so that the 1 bit at the end is not removed
        x_copy.insert(0, 0)
    return x_copy


# Finite field exponentiation
def power_of_three(x):
    multiplied = multiply(x, x)
    result = multiply(x, multiplied)
    return result

# Compute the value of the function F(x,k) = x^3+(x+k)^3+k using finite field operations
def F(x, k):
    return addition(addition(power_of_three(x), power_of_three(addition(x, k))), k)

# Convert list to string
def bits_to_string(bits):
    return ''.join(str(b) for b in bits)

# Converts a binary string to a list of bits
def string_to_bits(s):
    return [int(b) for b in s]

generate_lookup_table()

# Me and Seline Magnussen shared ideas on this problem, so the code can be similar even though we wrote them individually.