# To run the code you press run at it will create a text file with the 500 first output bits
def lfsr():

    state = [1] + [0]*28 + [1]

    # List to append all output bits to
    list_of_output = []

    #Using range 17 because 500/30 rounded up is 17
    for i in range(500):
        list_of_output.append(state[0])
        # Using polynomial x^30 + x^23 + x^2 + x + 1. x^30 = x^23 + x^2 + x + 1
        next_bit = (state[23] ^ state[2] ^ state[1] ^ state[0])
        state = state[1:] + [next_bit]


    # Find 500 first output bits
    string = ''.join(str(item) for item in list_of_output)

    # Writes the 500 first output bits to a text file
    with open('problem1_output.txt', 'w') as f:
        f.write(string)
        f.close()

lfsr()