"""This module implements a Wavelet tree"""

import time

class WaveletTree(object):
    """This class implements Wavelet tree structure"""
    def __init__(self, string):
        self.string = string
        self.root_node = WaveletNode()

        self.root_node.create_tree(self.string)

    def rank(self, position, character):
        """Delegates rank method to node"""
        return self.root_node.rank(position, character)

class WaveletNode(object):
    """This class implements a node in a Wavelet tree"""
    def __init__(self):
        self.char_dictionary = {}
        self.bit_vector = []
        self.alphabet_length = 0
        self.left = None
        self.right = None
        self.bit_pointer = {}

    def dictionary_init(self, alphabet):
        """Initialization of the alphabet dictionary"""
        if(self.alphabet_length > 2):
            middle_index = (len(alphabet) - 1) / 2
        else:
            middle_index = 1
            
        for char in alphabet[0 : middle_index]:
            self.char_dictionary[char] = 0
            
        for char in alphabet[middle_index : ]:
            self.char_dictionary[char] = 1

    def create_tree(self, string):
        """Creates Wavelet Tree for input string"""
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

    def rank(self, position, character):
        """Returns the number of occurences
        of "character" up to index "position" in a string.
        """
        bit = self.char_dictionary[character]
        bit_counter = 0

        # Counting the number of the same bit values as the character's bit
        for char in self.bit_vector[0 : position + 1]:
            if char == bit:
                bit_counter += 1

        # Recursively traversing child nodes
        if self.alphabet_length > 2:
            return self.bit_pointer[bit].rank(bit_counter - 1, character)
        else:
            # This is a leaf, we're done
            return bit_counter

class Fasta(object):
    """This class handles fasta file"""
    def __init__(self):
        self.conn_str = ""
        self.meta_data = ""
        self.data = ""
        self.length = -1

    def load(self, conn_str):
        """Loads fasta file"""
        self.conn_str = conn_str
        
        data = open(self.conn_str, 'r')
        header = data.readline().strip()

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
        genome.load("2.fasta")

        tree = WaveletTree(genome.data)
        length = genome.length
        print "A: " + str(tree.rank(length, 'A'))
        print "T: " + str(tree.rank(length, 'T'))
        print "G: " + str(tree.rank(length, 'G'))
        print "C: " + str(tree.rank(length, 'C'))

        execution_time = time.time() - start_time
        print execution_time

    except IOError:
        print "File doesn't exist"
