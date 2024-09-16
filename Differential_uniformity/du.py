import sys

# Finds the differential uniformity
def differential_uniformity(truth_table):
    n = len(truth_table[0][0]) # Length of bits
    max_diff = 0 # After the loop below finish running, this will be the differential uniformity.
    for i in range(1, 2**n): # Goes through all possible input differences except for 0
        a_str = format(i, '06b') # Turn the integer into a string
        a = string_to_bits(a_str) # Turn the string into a list of bits
        dict_count = {} # Keeps track of all output differences and how many times they occur for the current input difference
        for x, fx in truth_table:
            for y, fy in truth_table:
                if xor(x, y) == a:
                    b = bits_to_string(xor(fx, fy)) # Find output difference 
                    dict_count[b] = dict_count.get(b, 0) + 1 # Add output difference as key and 1 as value if it is first occurence. Add 1 to the value if output difference is already in dict.
        l = list(dict_count.values()) # Get the values as list so it can be sorted in descending order and thereafter get the first number in the list as that is the highest occurence of an output difference for the current input difference.
        l.sort(reverse=True)
        max_diff = max(max_diff, l[0]) # Update max_diff to the highest occurence of output difference for current input difference if the number is higher than the current value of max_diff. 
    return max_diff

# XOR the bits in list
def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

# Convert list to string
def bits_to_string(bits):
    return ''.join(str(b) for b in bits)

# Converts a binary string to a list of bits
def string_to_bits(s):
    return [int(b) for b in s]

# Reads from lookup table file and creates lists of bits.
def read_from_lookuptable(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lookup_table_list = []
        for line in lines:
            input_str, output_str = line.strip().split('->')
            lookup_table_list.append([string_to_bits(input_str), string_to_bits(output_str)])
        f.close()
    return lookup_table_list

# Main method used to take in arguments from terminal and print the result
def main():
    print(differential_uniformity(read_from_lookuptable(sys.argv[1])))

main()
