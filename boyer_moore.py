"""
@author: Grace Nathania
@created 25 March 2021

Codes for Boyer Moore algorithm with Galil's optimisation. One of the fastest pattern searching algorithms with complexity of O(N/M) with N as the length of the string and M as
the length of the pattern by using Bad Character rule, Good Suffix rule and matched prefix.
"""

from z_algorithm import z_algo
from z_algorithm import rev_z


def bad_character(pat):
    """
    This function creates a table to store the index of the rightmost occurrence
    of character in pattern. The column will be fixed at 256 according to the number
    of ASCII character yet the number of row will be based on unique character in pattern
    and row's length will be the length of the pattern.
    :param pat: the pattern (string) that will be preprocessed
    :Best case: O(m) with m as the length of the pattern
    This happen when pat only consists of 1 character
    :Worst case: O(m) with m as the length of the pattern
    This happen when pat consists of all ascii character
    :Space complexity: O(km) with k as the number of unique character in pat
    and m as the length of pattern
    :Auxiliary space complexity: O(kn) with k as the number of unique character in pat
    and n as the length of pattern
    :return bc_arr: an 2D array representing rightmost position of character in pattern
    """
    # Step 1 - Create a 2D array of size 256 since pat can be any ascii characters
    bc_arr = [None] * 256

    # Step 2 - Append an arr of len(pat) to bc_arr
    for i in range(len(pat)):
        idx = ord(pat[i])
        if bc_arr[idx] == None:
            bc_arr[idx] = [-1] * len(pat)

    # Step 3 - Loop through pat to fill in the table from the rightmost character in pat
    for i in range(len(pat) - 1, -1, -1):
        char = ord(pat[i])
        bc_arr[char][i] = i

        # Step 4 - Check value on the right; it it's 0, we replace it with current value
        for j in range(i, len(pat) - 1):
            if bc_arr[char][j + 1] == -1:
                bc_arr[char][j + 1] = i
            else:
                break

    # Step 5 - Return the array
    return bc_arr

def good_suffix(pat):
    """
    This function generates an array of good suffix whereby it stores the rightmost
    position of p in pat
    :param pat: the pattern (string) that will be preprocessed
    :Best case: O(m) with m as the length of pat. This happen when length of m = 1
    :Worst case: O(m) with m as the length of pat. This happen when length of m > 1
    :Space complexity: O(m) with m as the length of pat
    :Auxiliary space complexity: O(m) with m as the length of pat
    :return gs_arr: an array of length pat + 1
    """
    # Step 1 - Create good suffix array of size len(pat) + 1
    gs_arr = [0] * (len(pat) + 1)

    # Step 2 - Generate reversed z-arr for pat
    rev_z_arr = rev_z(pat)

    # Step 3 - Loop through reversed z-arr to fill in the good suffix array
    for p in range(len(rev_z_arr) - 1):
        j = len(pat) - rev_z_arr[p]
        gs_arr[j] = p

    # Step 4 - Return good suffix array
    return gs_arr

def matched_prefix(pat):
    """
    This function generates an array of good suffix whereby it stores the
    length of the longest suffix that is also the prefix of pat.
    :param pat: the pattern (string) that will be preprocessed
    :Best case: O(m) with m as the length of pat. This happen when length of m = 1
    :Worst case: O(m) with m as the length of pat. This happen when length of m > 1
    :Space complexity: O(m) with m as the length of pat
    :Auxiliary space complexity: O(m) with m as the length of pat
    :return matched_pref: an array of length pat + 1
    """
    # Step 1 - Generate z-arr for pat
    z_arr = z_algo(pat)

    # Step 2 - Initialise matched prefix array
    matched_pref = [0]

    # Step 3 - Loop through z-arr from the last index
    for i in range(len(z_arr) - 1, -1, -1):
        if z_arr[i] + i == len(pat):
            to_append = z_arr[i]

        else:
            if matched_pref == []:
                to_append = 0
            else:
                to_append = matched_pref[0]

        matched_pref.insert(0, to_append)

    # Step 4 - Return z-arr
    return matched_pref


def boyer_moore(txt, pat):
    """
    This function implements Boyer Moore algorithms to find the index where pat occurs in txt
    :param txt: the string that might contain pat
    :param pat: the pattern to be found in the text
    :Best Case: O(m + n/m) with n as the length of txt and m as the length of pat.
    The first m is for pat pre-processing and n/m for pat search in txt
    This happens when pat matches the txt
    :Worst Case: O(m + mn) if pat occurs in txt OR O(m + n) if pat does not occur in txt
    with n as the length of txt and m as the length of pat.
    :Space complexity: O(m+n) with n as the length of txt and m as the length of pat.
    :Auxiliary space complexity: O(m+n) with n as the length of txt and m as the length of pat.
    :return to_return: an array containing index(es) where pat is found in txt
    """
    # Step 1 - Base base when length txt is smaller than pat, pat won't be found in txt
    if len(txt) < len(pat):
        return []

    # Step 2 - Do pattern pre-processing (cost us O(3m) -> O(m))
    bc = bad_character(pat)
    gs = good_suffix(pat)
    mp = matched_prefix(pat)

    # Step 3 - Initialise necessary variable to trace txt and pat
    j = 0  # for txt
    m = len(pat) - 1 # for pat
    start = 0  # for Galil's
    stop = 0
    to_return = []

    # Step 4 - Align txt and pat, then trace txt from the left, and pattern from the right
    while (j + m) < len(txt):  # j+m
        k = m

        # when pat matches txt
        while pat[k] == txt[j + k] and k >= 0:
            k -= 1
            if k == stop: # Galil's optimisation
                k -= start

        # pattern matches the scanned txt[j...j + k]
        if k == -1:
            to_return.append(j + k + 1)

            # Case 2: calculate m - matched_pref[1] and take max value between it and 1
            j += max(1, m - mp[1] if m > 1 else 1)

        else:
            char = txt[j + k] # mismatched char in txt

            # Get shift value from bad character table and good suffix array
            if bc[ord(char)] == None:
                bc_val = 0
            else:
                bc_val = bc[ord(char)][k]

            bc_shift = max(1, k - bc_val)

            gs_shift = 1

            if gs[k + 1] > 0:
                gs_shift = m - gs[k + 1]

            elif gs[k + 1] == 0:
                gs_shift = m - mp[k + 1]

            shift = max(1, bc_shift, gs_shift) # Calculate shift distance

            # Determine if Galil's pointers need change (only if good suffix shift is used)
            if gs_shift >= bc_shift and gs_shift >= shift:
                start = k + m - (j+k)
                stop = k + m

            # Increment j
            j += shift

    # Step 5 - Return the array
    return to_return
