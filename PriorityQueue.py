"""
@author Grace Nathania
@created 29 June 2019
@modified 30 May 2020
"""

class PriorityQueue:
    """
    This class implements Minimum Heap / Priority Queue and is adapted from live coding
    session by Dr. Muhammad Fermi @Monash University Malaysia. This Priority Queue will
    store a tuple consisting of a key and a value in each node.
    """
    def __init__(self, size):
        """
        A constructor to initialise the priority queue by creating an array and set
        a counter to indicate the number of element(s) in the queue.
        """
        self.array = [None]*size
        self.counter = 0

    def is_empty(self):
        """
        A method that return a boolean indicating whether priority queue is empty or not
        :best and worst case: O(1)
        :aux space complexity: O(1)
        :space complexity: O(1)
        :return: True if array is empty and False if otherwise.
        """
        return self.counter == 0

    def __len__(self):
        """
        A method to calculate the number of element(s) in the queue.
        :best and worst case: O(1)
        :aux space complexity: O(1)
        :space complexity: O(1)
        :return: an integer indicating the number of element(s) in the queue.
        """
        return self.counter

    def __str__(self):
        """
        A method to print the priority queue
        :best case: O(N) with N as the number of element(s) in the queue. This happens
        when there is only 1 element in the array.
        :worst case: O(N) when array is full.
        :aux space complexity: O(N)
        :space complexity: O(N)
        :return: a string consisting of elements in the queue.
        """
        to_return = ""
        for i in range(self.counter + 1):
            to_return = to_return + str(self.array[i]) + ","

        return to_return

    def add(self, key, value):
        """
        A method to append an element, in the form of a tuple) to the queue.
        :param key: a key of the value. In this case, key is vertex ID.
        :param value: a value of the key. In this case, value is the distance to
        reach vertex ID.
        :best case: O(1) when array is full.
        :worst case: O(logN) with N as the number of element(s) in the queue because
        each time an element is inserted, rise happens.
        :aux space complexity: O(N) with N as the length of the queue.
        :space complexity: O(N)
        """
        if self.counter + 1 < len(self.array):
            self.array[self.counter + 1] = (key, value)
        else:
            raise Exception("Heap is full")

        self.counter += 1
        self.__rise(self.counter)

    def __rise(self, k):
        """
        A private method to perform rise. Rise happens to make the heap consistent as a
        minimum heap by swapping smaller child with its parents.
        :param k: the element's position that needs to be swapped.
        :best case: O(1) when k < 1 and child (self.array[k]) is smaller than its parents.
        :worst case: O(logN) with N as the number of element(s) in the queue. This happens
        when the value at position k is smaller than all the values in the queue.
        :aux space complexity: O(1) since no additional space is required.
        :space complexity: O(1)
        """
        while k > 1 and self.array[k][1] < self.array[k//2][1]:
            self.swap(k, k//2)
            k = k//2

    def serve(self):
        """
        A method to get the minimum value in the queue by changing the position of the child
        on the rightmost position with the first element. Then sink is called since the position
        of the first element is now bigger than its children.
        :best case: O(1) when queue is empty.
        :worst case: O(N) with N as the number of element(s) in the queue.
        :aux space complexity: O(1) since no additional space is required.
        :space complexity: O(1)
        :return: a tuple of minimum value.
        """
        if self.is_empty():
            raise Exception("Heap is empty")
        to_return = self.array[1]
        self.swap(1,self.counter)
        self.counter -= 1
        self.__sink(1)
        return to_return

    def __sink(self, k):
        """
        A private method to perform sink. sink happens to make the heap consistent as a
        minimum heap by swapping bigger parents with its child.
        :param k: the element's position that needs to be swapped.
        :best case: O(N) with N as the number of element(s) in the queue. This happens
        when the value of parents is smaller than the value of its child.
        :worst case: O(N) with N as the number of element(s) in the queue. This happens
        when the value at position k is bigger than all the values in the queue.
        :aux space complexity: O(1) since no additional space is required.
        :space complexity: O(1)
        """
        while 2*k <= self.counter:
            child = self.smallest_child(k)
            if self.array[k][1] <= self.array[child][1]:
                break
            self.swap(k, child)
            k = child

    def smallest_child(self, k):
        """
        A method to get the smalles child in the queue.
        :param k: the parents' position that needs to be checked.
        :best and worst case: O(1)
        :aux space complexity: O(1) since no additional space needed.
        :space complexity: O(1)
        :return: an index of 2*k when left child is smaller than right child
        or index of 2*k+1 when otherwise.
        """
        if 2*k == self.counter or self.array[2*k][1] < self.array[2*k+1][1]:
            return 2*k
        else:
            return 2*k + 1

    def swap(self, i, j):
        """
        A method to swap 2 elements in the queue.
        :param i: the element's position that needs to be swapped.
        :parma j: the element's position that needs to be swapped.
        :best and worst case: O(1)
        :aux space complexity: O(1) since no additional space needed.
        :space complexity: O(1)
        """
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def update(self, key, value):
        """
        A method to update the value in the queue. A rise will be performed
        if the new vallue is smaller while otherwise, a sink will be done.
        :param key: the key of which value to be updated
        :param value: the updated value
        :best and worst case: O(logN) when rise is performed and O(N) when
        sink is performed; N is the number of element(s) in the queue.
        :aux space complexity: O(1)
        :space complexity: O(1)
        """
        for i in range(1,self.counter+1):
            if self.array[i][0] == key:
                temp = self.array[i][1]
                self.array[i] = (key,value)
                if temp > value:
                    self.__rise(i)
                else:
                    self.__sink(i)
                break
