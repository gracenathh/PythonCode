"""
@author Grace Nathania
@created 24 March 2020
@modified 1: 26 March 2020
@modified 2: 28 March 2020
@modified 3: 31 March 2020
@modified 4: 4 April 2020
@modified 5: 9 April 2020

Code is adapted from live coding session by Dr. Ian Lim Wern Han
@Monash University Malaysia.
"""
import copy

def radix_sort(num_list,b):
    """
    This function will sort a list of integer(s) in increasing order using radix
    sort based on b. The implementation would be copying our num_list into another
    list since we cannot modify it. Then, we determine the maximum length of the
    greatest number in the list.

    To know how many times we have to perform counting sort, we have to know how long
    is our greatest number in num_list when it's represented in b. To do so, we
    calculate the result of floor division (//) of the number//base^power. Power will
    go all the way from 0 until M where the result of // is smaller than our base.

    Then, we initialise our count_array with the size of b and initialise another list
    inside each index of count_array. After doing all necessaries steps, we can perform
    counting sort for MN times to achieve our desired output. (Further explaination
    will be in the comments below)
    
    :precondition: num_list must consist integer(s), yet num_list can be empty too.
    b must be greater than 0.
    
    :param num_list: list of integers to be sorted
    :param b: base number
    
    :Best case: O(M(N+b)) when num_list is sorted with M as the length of the largest
    digit in terms of base b, N as the length of num_list, and b as base because num_list
    still has to go through the multiple counting sorts.
    
    :Worst case: O(M(N+b)) when num_list is unsorted with M as the length of the largest
    digit in terms of base b, N as the length of num_list, and b as base because num_list
    has to go through the multiple counting sorts.
    
    :Space complexity: O(MN+b+N) with M as the length of the largest digit in terms
    of base b, N as the length of num_list, and b as base.
    
    :Aux space complexity: O(N+b) with b as the base and N as the length of the num_list
    
    :return num_list_sorted: sorted list in ascending order.
    """
    
    #Step 1 - Copy num_list
    num_list_sorted = copy.deepcopy(num_list)


    #Step 2 - Look for which item has the longest length
    #Code below will run in O(N-1) time with N as the total item in the input list
    max_item = 0

    for i in range(len(num_list_sorted)):
        current_max_num = len(str(num_list_sorted[i]))
        if num_list_sorted[i] > max_item:
            max_item = num_list_sorted[i]

    max_item_length = len(str(max_item))

    #Step 3 - Find the number of digits of maxItem, when represented in base b
    #Code below will run in O(M) time with M as the number of digits of MaxItem,
    #represented in base b.
    convert_length = 1
    power = 0

    while (max_item//b**power) > b:
        convert_length += 1
        power += 1

    #Step 4 - Create count_array based on b
    #Code below will run in O(b) time with b as the base
    count_array = [0]*b
    for i in range(len(count_array)):
        count_array[i] = []

    #Step 5 - Create an outer loop for M times (M = the number of digits of
    #maxItem, when represented in base b) to ensure that numbers in our input
    #list are sorted based on the given b.
    
    for i in range(convert_length):
        for j in range(len(num_list_sorted)): #run in O(N) time
            index = (num_list_sorted[j]//b**i)%b
            count_array[index].append(num_list_sorted[j])

        #code below runs in O(ba) time with a as the length of count_array[j]
        index = 0
        for j in range(len(count_array)):
            for k in range(len(count_array[j])):
                num_list_sorted[index] = count_array[j].pop(0)
                index += 1

    #Step 6 - Return sorted list
    return num_list_sorted

def radix_sort_alpha(string_list):
    """
    This function will sort a list of string(s) in right-aligned (based on the length
    of the word(s) inside, from the shortest to the longest word). The implementation
    would be first copying our num_list into another list since we cannot modify it.
    Then, we determine the length of the longest word in the list.

    Since we have 26 alphabets, we will initialise a count_array of size 26 and put
    another list inside each index of count_array. After knowing the length of our
    longest word in the list and iniating a count_array, we can perform counting
    sort for MN times, with M as the lenght of the longest word in the list and N as
    the size of our string_list, to achieve our desired output. (Further explaination
    will be in the comments below)
    
    :precondition: string_list must consist string(s) in lower case with no special
    character, yet string_list can be empty too.
    
    :param string_list: list of strings to be sorted
    
    :Best case: O(MN) when string_list is sorted with M as the length of the longest
    string and N as the length of string because string_list still has to go through
    the multiple counting sorts.
    
    :Worst case: O(MN) when string_list is not sorted with M as the length of the
    longest word and N as the length of string because string_list still has to go
    through the multiple counting sorts.
    
    :Space complexity: O(M(N+1)) with M as the length of the longest string and N as
    the length of string
    
    :Aux space complexity: O(N) with N as the length of string_list
    
    :return word_list: sorted list in right-aligned.
    """

    #Step 1 - Copying input list into another list, run in O(N) time
    #with N as the length of string_list
    word_list = copy.deepcopy(string_list)

    #Step 2 - Looking for the length of the longest word in the list,
    #run in O(N) time.
    max_word_length = 0 #Initialise to 0 in case string_list is empty
    for word in word_list:
        if max_word_length < len(word):
            max_word_length = len(word)

    #Step 3 - Initialise count_array of size 26 since we have 26 alphabets
    #Also, initialise inner list, run in O(1) time.
    count_array = [0]*26 #aux space is used
    for i in range(26):
        count_array[i] = []

    #Step 4 - Performing radix sort from the last character of each word all
    #the way to the first character.
    index_to_int = -1

    #Outerloop runs in O(M) time; M = length of the longest word in the list
    for i in range(max_word_length): 
        for word in word_list: #innerloop 1 runs in O(N) time
            #at i-th iteration, where i >= length of current word, then we know
            #that list has been sorted and will be put in the first bucket of count_array
            if i >= len(word):
                count_array[0].append(word)
            else:
                letter = word[index_to_int] #take the most significant character to be converted
                letter_num = ord(letter) - 97
                count_array[letter_num].append(word) #appending the whole word to the "bucket"

        #performing sorting
        index = 0
        for j in range(len(count_array)):
            for k in range(len(count_array[j])):
                word_list[index] = count_array[j].pop(0)
                index += 1

        index_to_int -= 1

    #Step 5 - Returning sorted list
    return word_list
