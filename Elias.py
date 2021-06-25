"""
@author: Grace Nathania
@created 25 May 2021
"""
def to_binary(num):
    return bin(num)[2:]

def elias_num(num):
    # convert int dec to binary
    bin_val = to_binary(num)
    n = len(bin_val) - 1

    val = list(bin_val)
    while n >= 1:
        encoded_length = to_binary(n)
        # flip the first bit into 0
        # change to list first since string is immutable
        el_list = list(encoded_length)
        el_list[0] = "0"
        # change again into string representation
        #encoded_length = "".join(el_list)
        val = el_list + val
        n = len(el_list) - 1

    to_return = "".join(val)
    return to_return
  
def decode_elias(bitstr):
    # convert bitstr into a list
    bit_list = list(bitstr)
    start = 0
    stop = 1
    length = 0

    while bit_list[start] != "1":
        bit_list[start] = "1"

        shift = stop - start - 1
        for i in range(start, stop):
            length += (int(bit_list[i]) * (1 << shift))
            shift -= 1

        start = stop
        stop += length + 1
        length = 0

    # Decode num
    int_val = 0
    shift = stop - start - 1
    for i in range(start, stop):
        int_val += (int(bit_list[i]) * (1 << shift))
        shift -= 1

    return int_val
  
