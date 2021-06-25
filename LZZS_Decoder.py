"""
@author: Grace Nathania
@created: 25 May 2021
"""

def decode_lzss(code_list):
    to_return = ""

    for code in code_list:
        bit = code[0]

        if bit == 1:
            char = code[1]
            to_return += char
            continue

        elif bit == 0:
            offset = code[1]
            length = code[2]
            idx = len(to_return) - offset

            for i in range(length):
                to_return += to_return[idx]
                idx += 1

        else:
            raise Exception ("Not LZSS")

    return to_return

lst = [(1,"a"),(1,"a"),(1,"c"),(0,3,4),(1,"b"),(0,3,3),(1,"a")]
print(decode_lzss(lst))
