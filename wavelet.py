"""
This module implements a Wavelet tree
"""

import time
import resource
import sys

class WaveletTree(object):
    """
    This class implements Wavelet tree structure
    """
    def __init__(self, data):
        """
        Creates wavelet tree from the data given

        :param data: data loaded from the file from which we're
            creating the tree
        """
        self.data = data
        self.root_node = WaveletNode()

        self.root_node.create_tree(self.data)

    def rank(self, position, character):
        """
        Delegates rank method to node and returns rank
        of the character at certain position
        """
        return self.root_node.rank(position, character)

class WaveletNode(object):
    """
    This class implements a node in a Wavelet tree
    """
    def __init__(self):
        """
        Initialization of the class attributes

        :attribute char_dictionary: every character of the alphabet
            gets a bit value (0 or 1)
        :attribute bit_vector: list of values (0 or 1) for every
            character in the string
        :attribute left and right: references to left and right
            (child) nodes
        :attribute bit_pointer: pointer to (child) node reference
            for every character of the alphabet in the current node
        """
        self.char_dictionary = {}
        self.bit_vector = []
        self.alphabet_length = 0
        self.left = None
        self.right = None
        self.bit_pointer = {}

    def dictionary_init(self, alphabet):
        """
        Initialization of the alphabet dictionary
        
        :param alphabet: list of all the (different) characters in the data
        """
        if(self.alphabet_length > 2):
            """
            even-length alphabets get sliced in the middle,
            at odd-length ones left node gets one character more
            """
            middle_index = ((len(alphabet) + 1) / 2)
        else:
            middle_index = 1
            
        for char in alphabet[0 : middle_index]:
            self.char_dictionary[char] = 0
            
        for char in alphabet[middle_index : ]:
            self.char_dictionary[char] = 1

    def create_tree(self, string):
        """
        Recursively creates wavelet tree for input string

        :param string: data from which we're creating the node
        """
        alphabet = []
        left_string = ""
        right_string = ""
        
        # Creating alphabet
        for char in string:
            if char not in alphabet:
                alphabet.append(char)

        # Alphabet needs to be sorted before proceeding
        alphabet.sort()

        self.alphabet_length = len(alphabet)
        self.dictionary_init(alphabet)

        # If alphabet length is bigger than 2, then we're dealing with a node
        if self.alphabet_length > 2:
            # Creating filtered strings for left and right node
            for char in string:
                bit_value = self.char_dictionary[char]
                self.bit_vector.append(bit_value)
                
                if bit_value is 0:
                    left_string += char
                else:
                    right_string += char

            # Creating new nodes and recursively calling create_tree method
            self.left = WaveletNode()
            self.bit_pointer[0] = self.left
            self.left.create_tree(left_string)

            self.right = WaveletNode()
            self.bit_pointer[1] = self.right
            self.right.create_tree(right_string)

        else:
            # This is a leaf
            for char in string:
                bit_value = self.char_dictionary[char]
                self.bit_vector.append(bit_value)

    def rank(self, index, character):
        """
        Returns the number of occurences
        of character up to specified index in a string.
        """
        bit = self.char_dictionary[character]
        bit_counter = 0

        # Counting the number of the same bit values as the character's bit
        for char in self.bit_vector[0 : index + 1]:
            if char == bit:
                bit_counter += 1

        # Recursively traversing child nodes
        if self.alphabet_length > 2:
            return self.bit_pointer[bit].rank(bit_counter - 1, character)
        else:
            # This is a leaf, we're done
            return bit_counter

class Fasta(object):
    """
    This class handles fasta file
    """
    def __init__(self):
        """
        Data initialization
        """
        self.conn_str = ""
        self.meta_data = ""
        self.data = ""
        self.length = -1

    def load(self, conn_str):
        """
        Loads fasta file
        """
        self.conn_str = conn_str
        
        data = open(self.conn_str, 'r')
        header = data.readline().strip()

        #if added, storing header into meta_data
        if(header[0] == '>'):
            self.meta_data = header
        # Ignoring comments
        elif header[0] == ';':
            pass
        else:
            self.data += header

        for line in data:
            if line[0] != ';':
                self.data += line.strip()

        self.length = len(self.data)


if __name__ == "__main__":

    start_time = time.time()
    genome = Fasta()
    
    try:
        # file path as command line argument
        file_path = sys.argv[1]
        character = ""
        genome.load(file_path)

        # populate the tree with data read from the file
        tree = WaveletTree(genome.data)
        
        execution_time = time.time() - start_time

        print
        print "Executed in: " + str(execution_time) + " seconds"
        # function for measuring  memory usage
        print "Memory used: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + " kB"
        print

        # check the rank of the character
        while 1:
            print "Run 'rank' function for character (enter character) or exit with 'c': "
            character = str(raw_input())
            if character == 'c':
                break
            else:
                length = genome.length
                try:
                    print character + ": " + str(tree.rank(length, character))
                except KeyError:
                    print "Character doesn't exist (and is case-sensitive)"
                    break

    except IOError:
        print "File doesn't exist"
