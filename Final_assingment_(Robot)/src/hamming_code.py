#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union
from functools import reduce


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'



class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
    
        gns = [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self,gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION

        k = 10

        for K in range(k):
            gns[2][K] = abs(gns[2][K] - gns[0][K]) % 2
            gns[4][K] = abs(gns[4][K] - gns[0][K]) % 2
            gns[5][K] = abs(gns[5][K] - gns[0][K]) % 2

        for K in range(k):
            gns[0][K] = abs(gns[0][K] - gns[1][K]) % 2
            gns[2][K] = abs(gns[2][K] - gns[1][K]) % 2
            gns[5][K] = abs(gns[5][K] - gns[1][K]) % 2

        for K in range(k):
            gns[0][K] = abs(gns[0][K] - gns[2][K]) % 2
            gns[4][K] = abs(gns[4][K] - gns[2][K]) % 2
            gns[5][K] = abs(gns[5][K] - gns[2][K]) % 2

        for K in range(k):
            gns[0][K] = abs(gns[0][K] - gns[3][K]) % 2
            gns[2][K] = abs(gns[2][K] - gns[3][K]) % 2

        for K in range(k):
            gns[1][K] = abs(gns[1][K] - gns[4][K]) % 2
            gns[2][K] = abs(gns[2][K] - gns[4][K]) % 2

        for K in range(k):
            gns[0][K] = abs(gns[0][K] - gns[5][K]) % 2
            gns[1][K] = abs(gns[1][K] - gns[5][K]) % 2
            gns[4][K] = abs(gns[4][K] - gns[5][K]) % 2
        return gns   

    
    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #Getting Parity matrix parity_mat from G 
        parity_mat = [row[6:] for row in g]
        
        #Getting identity matrix identity_mat(n-k)
        identity_mat = [[1 if a == b else 0 for b in range(4)] for a in range(4)]

        # Build H mat from parit_mat and identity_mat in the format [H] = [parity_mat(transpose) | identity_mat]
        parity_mat_trans = [list(t) for t in zip(*parity_mat)]
        h_mat = [x+y for x, y in zip(parity_mat_trans, identity_mat)]
        
        return h_mat



    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        if len(source_word) != 6:
            return None
         
        gns = self.g
        code_word = []

        #Getting transpose of matrix G' for multiplication 
        gns_trans = [list(t) for t in zip(*gns)]
        #print(gns_trans)
        

        #performs an element-wise multiplication of the transposed matrix gns_trans with source_word
        temp_mat = [[x&y for x, y in zip(list(source_word), gns_trans[i])] for i in range(len(gns_trans))]

        #XOR reduction on the elements of each row to obtain the individual binary elements of the code_word
        for row in temp_mat:
            code_word.append(reduce(lambda a,b: a^b, row))

        # Adding overall parity bit
        code_word.append(reduce(lambda x,y: 1 if(x^y) else 0, code_word))
        return tuple(code_word)



    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION

        if len(encoded_word) != 11:
            return tuple([None, HCResult.UNCORRECTABLE])

        h = self.h
        syndrome = []
        code_word_r = list(encoded_word)
        overall_parity_bit = sum(code_word_r)
        code_word_r.pop()
        mid_result = [[x&y for x, y in zip(code_word_r, h[i])] for i in range(len(h))]
        for row in mid_result:
            syndrome.append(reduce(lambda a,b: a^b, row))
        # Getting transpose of H to compare with Syndrome to identify errors
        h_trans = [list(t) for t in zip(*self.h)]
        #print ("H_trans = ", h_trans)
        if all([v == 0 for v in syndrome]) and overall_parity_bit % 2==0:
          return tuple(code_word_r[0:6]), HCResult.VALID                          
        elif all([v == 0 for v in syndrome]) and overall_parity_bit % 2==1:
          return tuple(code_word_r[0:6]), HCResult.CORRECTED                                                               
        elif syndrome in h_trans and overall_parity_bit % 2==1:
            for k in range(0,10):
                if syndrome==h_trans[k]:
                    code_word_r[k]=(0 if code_word_r[k]==1 else 1)
            return tuple(code_word_r[0:6]), HCResult.CORRECTED
        else:
            return None, HCResult.UNCORRECTABLE