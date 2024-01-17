#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


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
        gns = [
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        ]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        gen = gns

        gen[2] = [x ^ y for x, y in zip(gen[2], gen[0])]
        gen[4] = [x ^ y for x, y in zip(gen[4], gen[0])]
        gen[5] = [x ^ y for x, y in zip(gen[5], gen[0])]
        gen[0] = [x ^ y for x, y in zip(gen[0], gen[1])]
        gen[2] = [x ^ y for x, y in zip(gen[2], gen[1])]
        gen[5] = [x ^ y for x, y in zip(gen[5], gen[1])]
        gen[0] = [x ^ y for x, y in zip(gen[0], gen[2])]
        gen[4] = [x ^ y for x, y in zip(gen[4], gen[2])]
        gen[5] = [x ^ y for x, y in zip(gen[5], gen[2])]
        gen[0] = [x ^ y for x, y in zip(gen[0], gen[3])]
        gen[2] = [x ^ y for x, y in zip(gen[2], gen[3])]
        gen[1] = [x ^ y for x, y in zip(gen[1], gen[4])]
        gen[2] = [x ^ y for x, y in zip(gen[2], gen[4])]
        gen[0] = [x ^ y for x, y in zip(gen[0], gen[5])]
        gen[1] = [x ^ y for x, y in zip(gen[1], gen[5])]
        gen[4] = [x ^ y for x, y in zip(gen[4], gen[5])]

        return gen

    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List): Systematic generator matrix
        Returns:
            list: Derived parity-check matrix
        """
        aux = [row[-4:] for row in g]
        a = list(map(list, zip(*aux)))

        #a = [[row[i] for row in [row[5:] for row in g[:5]]] for i in range(self.parity_bits)]
        id = [[1 if i == j else 0 for j in range(self.total_bits - self.data_bits)] for i in
              range(self.total_bits - self.data_bits)]
        return [rowa + rowid for rowa, rowid in zip(a, id)]

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """
        source_word = list(source_word)
        if len(source_word) != 6:
            return None
        res = [sum(x * y for x, y in zip(source_word, rowg)) for rowg in zip(*self.g)]
        res = [x % 2 for x in res]
        n = 0
        for i in res:
            if i == 1:
                n += 1
        if (n % 2) == 0:
            res.append(0)
        else:
            res.append(1)
        return tuple(res)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """
        encoded_word = list(encoded_word)
        if len(encoded_word) != 11:
            return tuple([None, HCResult.UNCORRECTABLE])

        parity = 0
        perr = False
        for b in encoded_word[:10]:
            if b == 1:
                parity += 1
        if parity % 2 != encoded_word[10]:
            perr = True

        aux = [[b] for b in encoded_word[:10]]
        syn = [[0], [0], [0], [0]]
        for i in range(len(self.h)):
            for j in range(len(aux[0])):
                for k in range(len(aux)):
                    syn[i][j] += self.h[i][k] * aux[k][j]
        syn = [b for row in syn for b in row]
        syn = [b % 2 for b in syn]

        error = not all(b == 0 for b in syn)

        if not error and not perr:
            return tuple([tuple(encoded_word[:6]), HCResult.VALID])
        elif not error and perr:
            return tuple([tuple(encoded_word[:6]), HCResult.CORRECTED])
        elif error and perr:
            pos = -1
            for column in range(len(self.h[0])):
                col = [self.h[row][column] for row in range(len(self.h))]
                if col == syn:
                    pos = column
                    break
            if pos != -1:
                if encoded_word[pos] == 1:
                    encoded_word[pos] = 0
                else:
                    encoded_word[pos] = 1
                return tuple([tuple(encoded_word[:6]), HCResult.CORRECTED])
            else:
                return tuple([None, HCResult.UNCORRECTABLE])
        else:
            return tuple([None, HCResult.UNCORRECTABLE])
