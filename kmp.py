"""
@author: Grace Nathania
@created 24 March 2021

KMP algorithm is used for pattern searching. It uses longest proper suffix of pattern[1...i] that matches a prefix of the pattern, such that pat[i+1] != pat[SPi+1]. 
This algorithm runs in O(M+N) time with M as the length of the pattern and N as the length of the string.
"""
from z_algorithm import z_algo

def spi(pat):
    m = len(pat)
    spi_arr = [0]*len(pat)
    z_arr = z_algo(pat)

    for j in range(len(pat)-2,1,-1):
        i = j + z_arr[j] - 1
        spi_arr[i] = z_arr[j]

    return spi_arr

def kmp(txt, pat):
    n = len(txt)
    m = len(pat)
    to_return = []
    spi_arr = spi(pat)
    j = 0

    while j <= n - m:
        i = 0
        while i < m:
            if pat[i] != txt[i+j]:
                break
            i += 1

        if i == m:
            to_return.append(j)
            shift = m - spi_arr[m-1]

        else:
            shift = i - spi_arr[i-1]

        shift = max(1, shift)
        j += shift

    return to_return
