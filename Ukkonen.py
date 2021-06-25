"""
@author: Grace Nathania
@created 30 April 2021

This code represents Ukkonen's Suffix Tree Construction algorithm along with finding suffix array and longest common prefix using generalised suffix tree. 
All are computed in O(N) time with N as the length of the string.
"""

class Node:
    """
    A class to implement a Node for Suffix Tree. Node is a list of size 27,
    allocating first position to indicate the end of Node (terminal) and the rest
    to indicate lower case English characters.
    """
    def __init__(self, start, end, leaf = True):
        """
        Construction function that initialises instances of class Node
        """
        self.child = None
        self.suffix_link = None
        self.leaf = leaf

        # Trick 2 - Edge representation
        self.start = start
        self.end = end

        self.child_count = 0

        if not leaf:
            self.leaf = False
            self.child = [None]*27

    def get_child(self, i):
        """
        This function return Node's child of index i
        :param i: the location of the child
        :Best and worst case: O(1) since it is a direct access to child's location
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return: Node's child at position i
        """
        return self.child[i]

    def add_child(self, i, new_child):
        """
        This function add child (Node) of the current node at index i
        :param i: the location of new child
        :param new_child: a node acts as the child of the current node
        :Best and worst case: O(1) since it is just increasing child_count and a direct access
        to child's location
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return: None
        """
        self.child_count += 1
        self.child[i] = new_child

    def edge_len(self):
        """
        This function calculate the length of Node's length
        :Best and worst case: O(1) since it is just simple if else and calculation
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return: None
        """
        end_idx = self.end if isinstance(self.end, int) else self.end.get_value()
        return end_idx - self.start + 1

class EndPointer:
    """
    A class to implement EndPointer of a node for Trick 1 of Ukkonen implementation:
    once a leaf, always a leaf.
    """
    def __init__(self):
        """
        Construction function that initialises instances of class EndPointer
        """
        self.value = None

    def set_value(self, end):
        """
        This function sets value for EndPointer
        :param end: the value for EndPointer
        :Best and worst case: O(1)
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return: None
        """
        self.value = end

    def get_value(self):
        """
        This function gets value of EndPointer
        :Best and worst case: O(1)
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return self.value: value of EndPointer
        """
        return self.value

class SuffixTree:
    """
    A class to implement Ukkonen's suffix tree algorithm.
    """

    def __init__(self, text):
        """
        Construction function that initialises instances of class SuffixTree

        This function also initiates the tree construction by creating root node,
        setting active length to 0, setting root's suffix link, and calling build_tree function.
        """
        self.text = text
        self.size = len(text)

        self.end_pointer = EndPointer()
        self.j = 0

        self.active_edge = -1
        self.previous_node = None
        self.active_length = 0

        # Creating the suffix tree
        self.root = Node(-1,-1, False)
        self.root.suffix_link = self.root
        self.active_node = self.root

        self.build_tree()

    def build_tree(self):
        """
        This function build the tree for all characters in self.text
        :Best case: O(1) when there is only 1 character in self.text
        :Worst case: O(n) with n as the length of self.text
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return: None
        """
        for i in range(self.size):
            self.extendSuffixTree(i)

    def add_node(self, start, end, leaf = True):
        """
        This function creates a new node that is linked to the self.root
        :param start: the start index of character(s) in self.text at the node
        :param end: the end index of character(s) in self.text at the node
        :param leaf: condition if the new node is the end of the tree or not
        :return new_node: a new node
        """
        new_node = Node(start, end, leaf)
        new_node.suffix_link = self.root
        return new_node

    def get_index(self, char):
        """
        This function finds the ascii code for a character in self.text
        :param char: the character that its ascii code is to be found
        :Best and Worst complexity: O(1) since it is just if condition and return
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return an ascii index of the char - 96 to fits into the child array of size 27.
        This return 0 IF the character is a terminal ($)
        """
        if char == "$":
            return 0
        return ord(char)-96

    def skip_count(self, node):
        """
        This function implements Trick 3 of skip count to avoid traversing 1 letter at a
        time when we know the[start, end] of an edge by giving a condition whether an edge
        can be skipped or not
        :param node: a node that its edge will be checked
        :Best and Worst complexity: O(1) because it's just an if statement and a return
        :Aux space complexity: O(1)
        :Space complexity: O(1)
        :return True if we can skip an edge and False if we cannot skip an edge
        """
        if self.active_length >= node.edge_len():
            self.active_node = node
            self.active_length -= node.edge_len()
            self.active_edge += node.edge_len()
            return True
        return False

    def extendSuffixTree(self, i):
        """
        This function extends the suffix tree by adding new nodes, branching, etc.
        :param i: a pointer of where the construction will begin
        :Best complexity: O(1) when the value of i and j are the same, thus while loop
        only happens once
        :Worst complexity: O(n) with n as self.size and this happens when pointer-i is at 0
        and pointer-j is at the last character in self.text
        :Aux space complexity: O(1) because no array is required in this function
        :Space complexity: O(1)
        :return: None
        """

        # Step 1 - Setting previous node as None when entering new phase
        self.previous_node = None

        # Trick 1 - Once a leaf, always a leaf
        self.end_pointer.set_value(i)

        # Step 2 - Looping through from j to i
        while (self.j <= i):
            if self.active_length == 0:
                self.active_edge = i

            # Rule 1 - Add letter to leaf
            # Checking if there is an active node, if there is not, create new node
            idx_ae = self.get_index(self.text[self.active_edge])

            if self.active_node.get_child(idx_ae) is None:
                new_child = self.add_node(i, self.end_pointer)
                self.active_node.add_child(idx_ae, new_child)

                # Creating suffix link if branching happens
                if self.previous_node is not None:
                    self.previous_node.suffix_link = self.active_node
                    self.previous_node = None

            # active node exists and has child
            else:
                next = self.active_node.get_child(idx_ae)

                # Trick 3 - Skip Count
                # updating active node and traversing to the internal node
                if self.skip_count(next):
                    continue

                # Rule 3 - already exists
                if self.text[i] == self.text[next.start + self.active_length]:
                    if self.active_node != self.root and self.previous_node is not None:
                        self.previous_node.suffix_link = self.active_node
                        self.previous_node = None

                    # Trick 4 - Showstopper
                    self.active_length += 1
                    break

                # Rule 2 - add branch (new node)
                new_start = next.start
                next.start += self.active_length

                branch_node = self.add_node(new_start, new_start + self.active_length-1, False)
                branch_node.add_child(self.get_index(self.text[next.start]), next)
                branch_node.add_child(self.get_index(self.text[i]), self.add_node(i, self.end_pointer))

                # Connecting active node to branch_node
                self.active_node.child[self.get_index(self.text[new_start])] = branch_node

                # if at the same phase an internal node was created in the last extension, suffix_link is created to branch_node
                if self.previous_node is not None:
                    self.previous_node.suffix_link = branch_node
                self.previous_node = branch_node

            self.j += 1

            # updating active edge and length for next iteration
            if self.active_node == self.root and self.active_length > 0:
                self.active_edge = self.j
                self.active_length -= 1
            else:
                self.active_node = self.active_node.suffix_link
                
    def L(self, i, j):
        """
        This function finds the LCP of text-1 from index i and text-2 from index j.
        :param i: Starting position of text one
        :param j: Starting position of text two
        :Best complexity: O(1) when the first character of text one at index i and
        the first character of text two at index j are not the same
        :Worst complexity: O(d) with d as the number of DFS function being called
        :Aux space complexity: O(1) since no array is included
        :Space complexity: O(1)
        :return result: an array consisting of tuple of i,j and length of LCP
        """
        result = 0
        j += (self.dollar_idx + 1)

        if i > self.dollar_idx or i < 0 or j > self.hash_idx or j < self.dollar_idx - 1:
            return result

        root_child = self.root.child

        i_idx = self.get_index(self.text[i], i)
        j_idx = self.get_index(self.text[j], j)

        if i_idx != j_idx:
            return result

        else: # path exists, call dfs to find LCP
            if root_child[i_idx] is not None:
                result += self.dfs(root_child[i_idx], i, j, 0)
        return result

    def dfs(self, node, i, j, lcp_len):
        """
        This function performs depth-first search (DFS) starting from node input to
        calculate the length of LCP.
        :param node: The starting node to be traced
        :param i: Starting position of text one
        :param j: Starting position of text two
        :param lcp_len: length of the characters that share the same edge(s)
        :Best complexity: O(1) when char at index i + edge_len in text one is not
        the same as char at index j + edge_len in text two.
        :Worst complexity: O(d) with d as the number of dfs being called.
        :Aux space complexity: O(1) since no array is included
        :Space complexity: O(1)
        :return current_len: the length of LCP
        """
        current_len = lcp_len
        edge_len = node.edge_len()

        current_len += edge_len
        i += edge_len
        j += edge_len

        i_idx = self.get_index(self.text[i], i)
        j_idx = self.get_index(self.text[j], j)

        # Recursively calling dfs function again since we know when i_idx and j_idx are
        # the same, the LCP length might be longer
        if i_idx == j_idx:
            return self.dfs(node.child[i_idx], i, j, current_len)

        # No more match is found, thus we return the length of LCP
        return current_len
                
class SuffixArray:
    """
    A class to implement Suffix Array
    """

    def __init__(self, text, tree):
        """
        Construction function that initialises instances of class SuffixArray
        """
        self.text = text
        self.text_size = len(text)
        self.tree = tree
        self.suffix_arr = self.trace_tree(self.tree.root, 0)

    def trace_tree(self, node, n):
        """
        This function trances the Suffix Tree to obtain Suffix Array (in-order traversal)
        :param node: The start node of the tracing
        :param n: the number/length of character that we have traced so far
        :Best case: O(1) when there is only 1 child node that is also a leaf
        :Worst case: O(M) with M as the number of leaf in the tree (# of suffix array)
        :Aux space complexity: O(M) with M as the number of leaf in the tree (to_return array)
        :Space complexity: O(M) with M as the number of leaf in the tree (to_return array)
        :return:
        """
        to_return = []
        total_len = n

        # Looping through the child of node to check which one has another child
        for i in range(27):
            child = node.child[i]
            if child is not None:
                current_edge = child.edge_len()
                if child.leaf:
                    # index is calculated from text_size - length of all the characters we have traced
                    suffix_idx = self.text_size - (total_len + current_edge)
                    to_return.append(suffix_idx)
                else:
                    # Calling the trace function again to reach the leaf and get the index
                    to_return = to_return + self.trace_tree(child, total_len + current_edge)

        return to_return

if __name__ == "__main__":
    text_one = open("text_one.txt","r")
    text_two = open("text_two.txt","r")
    pair = open("pair.txt","r")

    pair_list = []
    for line in pair:
        line = line.strip()
        line = line.split(" ")
        pair_list.append(line)

    add_text = ""
    for text in text_one:
        add_text += (text + "$")
    for text in text_two:
        add_text += (text + "#")

    tree = SuffixTree(add_text)

    result_list = []

    for i,j in pair_list:
        lcp = tree.L(int(i), int(j))
        result_list.append([int(i), int(j), lcp])
