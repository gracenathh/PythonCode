"""
@author: Grace Nathania
@created 26 March 2021
"""

def z_algo(txt):
    """
    This function represents Gausfield's Z-Algorithm.
    :param txt: a string contains pattern + $ + text
    :Best case: O(N+M) with N as the length of the pattern and M as the length of the text.
    This happens when there is no pattern's occurrences in the text, thus we only do naive comparison.
    :Worst case: O(N+M) with N as the length of the pattern and M as the length of the text.
    This happens when pattern and text have the same characters, thus after naive comparison, we still need to check
    the value inside the z-box.
    :Space complexity: O(N+M) with N as the length of the pattern and M as the length of the text for the z_array
    :Aux space complexity: O(1)
    :return z_array: an array containing the occurrences of the pattern in the text
    """

    # Step 1 - Initialise z-array with the length of txt and insert length of txt into z_arr[0]
    z_arr = [0] * len(txt)
    z_arr[0] = len(txt)

    # Step 2 - Set left, right, and k pointers to 0
    l = r = k = 0

    # Step 3 - Loop through the txt starting from position 1
    for i in range(1, len(txt)):
        # case 1: i is outside the z-box -> do naive comparison
        if i > r:
            l,r = i,i

            while r < len(txt) and txt[r-l] == txt[r]:
                r += 1
            z_arr[i] = r - l
            r -= 1

        # case 2: i is inside the z-box
        else:
            # find k index first
            k = i - l

            # find the remaining
            rem = r - i + 1

            # case 2a: z[k] < remaining -> z[i] = z[k]
            if z_arr[k] < rem:
                z_arr[i] = z_arr[k]

            # case 2b: z[k] > remaining -> z[i] = remaining
            elif z_arr[k] > rem:
                z_arr[i] = rem

            # case 2c: z[k] == remaining
            else:
                # compare all additional character
                new_r = r + 1

                while new_r < len(txt) and txt[new_r-i] == txt[new_r]:
                   new_r += 1
                z_arr[i] = new_r - i

                l = i
                r = new_r - 1

    # Step 4 - Return z_arr
    return z_arr

def rev_z(txt):
    """
    This function is a reverse function of Gausfield's Z-Algorithm.
    :param txt: a string contains text + $ + pattern.
    The placement of text and pattern are switch since we are calculating reverse z-algorithm
    :Best case: O(N+M) with N as the length of the pattern and M as the length of the text.
    This happens when there is no pattern's occurrences in the text, thus we only do naive comparison.
    :Worst case: O(N+M) with N as the length of the pattern and M as the length of the text.
    This happens when pattern and text have the same characters, thus after naive comparison, we still need to check
    the value inside the z-box.
    :Space complexity: O(N+M) with N as the length of the pattern and M as the length of the text for the z_array
    :Aux space complexity: O(1)
    :return z_array: an array containing the occurrences of the pattern in the text
    """

    # Step 1 - Initialise z-array with the length of txt and insert length of txt into z_arr[-1]
    z_arr = [0] * len(txt)
    z_arr[-1] = len(txt)

    # Step 2 - Set left, right, and k pointers to length(text) - 1 and rplus = 1 as the offset to calculate k
    l = r = k = len(txt) - 1
    rplus = 1

    # Step 3 - Loop through the txt starting from the last position + 1
    for i in range(z_arr[-1] - 2, -1, -1):
        # case 1: i is outside the z-box -> do naive comparison
        if i < l:
            if rplus + i != len(z_arr) - 1:
                rplus = len(z_arr) - i - 1

            l, r = i, i

            while l > -1 and txt[r + rplus] == txt[l]:
                l -= 1
                rplus -= 1

            z_arr[i] = r - l

            if z_arr[i] == 0:
                rplus += 1
            else:
                rplus += z_arr[i]
                l += 1

        else:
            # find k
            k = i + rplus

            # find remaining
            rem = i - l + 1

            # case 2a: z[k] < remaining -> z[i] = z[k]
            if z_arr[k] < rem:
                z_arr[i] = z_arr[k]

            # case 2b: z[k] > remaining -> z[i] = remaining
            elif z_arr[k] > rem:
                z_arr[i] = rem

            # case 2c: z[k] == remaining
            # compare all additional character
            else:
                new_l = l - 1

                while new_l > -1 and txt[len(z_arr) - 1 - (i - new_l)] == txt[new_l]:
                    new_l -= 1

                z_arr[i] = i - new_l

                r = i
                l = new_l + 1
                rplus = len(z_arr) - 1 - r

    # Step 4 - Return z_arr
    return z_arr
