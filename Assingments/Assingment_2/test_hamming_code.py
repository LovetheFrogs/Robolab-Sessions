#!/usr/bin/env python3
from hamming_code import HCResult, HammingCode
import unittest


class TestHammingCode(unittest.TestCase):
    def test_instance(self):
        """ Essential: Test class instantiation """
        hamming = HammingCode()
        print(hamming.decode(tuple([0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1])))
        print(hamming.decode(tuple([0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0])))
        print(hamming.decode(tuple([0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1])))
        assert hamming.data_bits == 6

    def test_invalid_codes(self):
        """ Added: Check if the code to encode/decode is valid """
        hamming = HammingCode()
        assert hamming.encode(tuple([0, 0])) is None
        assert hamming.encode(tuple([0, 1, 1, 0, 0, 0, 1, 1])) is None
        assert hamming.decode(tuple([0, 1, 1]))[0] is None
        assert hamming.decode(tuple([0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]))[0] is None

    def test_encode_decode(self):
        """ Added: Test encoding and then decoding of a word """
        hamming = HammingCode()
        assert hamming.decode(hamming.encode(tuple([0, 1, 1, 0, 1, 1])))[0] == tuple([0, 1, 1, 0, 1, 1])
        assert hamming.decode(hamming.encode(tuple([1, 1, 0, 0, 0, 1])))[0] == tuple([1, 1, 0, 0, 0, 1])

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        hamming = HammingCode()
        assert hamming.decode(tuple([0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]))[0] == tuple([0, 1, 1, 0, 1, 1])
        assert hamming.decode(tuple([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))[0] == tuple([0, 0, 0, 0, 0, 0])
        assert hamming.decode(tuple([1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1]))[0] == tuple([1, 0, 1, 1, 0, 1])
        assert hamming.decode(tuple([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]))[0] == tuple([1, 1, 1, 1, 1, 0])

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        hamming = HammingCode()
        assert hamming.decode(tuple([1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1]))[0] == tuple([1, 1, 1, 1, 1, 0])
        assert hamming.decode(tuple([1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1]))[1] == HCResult.CORRECTED
        assert hamming.decode(tuple([0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0]))[0] == tuple([0, 1, 1, 0, 1, 1])
        assert hamming.decode(tuple([0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0]))[1] == HCResult.CORRECTED
        assert hamming.decode(tuple([1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1]))[0] == tuple([1, 1, 0, 0, 0, 1])
        assert hamming.decode(tuple([1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1]))[1] == HCResult.CORRECTED
        assert hamming.decode(tuple([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))[0] == tuple([0, 0, 0, 0, 0, 0])
        assert hamming.decode(tuple([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))[1] == HCResult.CORRECTED

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        hamming = HammingCode()
        assert hamming.decode(tuple([1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1]))[0] is None
        assert hamming.decode(tuple([1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1]))[1] == HCResult.UNCORRECTABLE
        assert hamming.decode(tuple([1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]))[0] is None
        assert hamming.decode(tuple([1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]))[1] == HCResult.UNCORRECTABLE
        assert hamming.decode(tuple([1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]))[0] is None
        assert hamming.decode(tuple([1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]))[1] == HCResult.UNCORRECTABLE
        assert hamming.decode(tuple([0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]))[0] is None
        assert hamming.decode(tuple([0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]))[1] == HCResult.UNCORRECTABLE

    def test_encode(self):
        """ Essential: Test method encode() """
        hamming = HammingCode()
        assert hamming.encode(tuple([0, 1, 1, 0, 1, 1])) == tuple([0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0])
        assert hamming.encode(tuple([0, 0, 0, 0, 0, 0])) == tuple([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert hamming.encode(tuple([1, 0, 1, 1, 0, 1])) == tuple([1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1])
        assert hamming.encode(tuple([1, 1, 1, 1, 1, 0])) == tuple([1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1])
        assert hamming.encode(tuple([1, 1, 0, 0, 0, 1])) == tuple([1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1])


if __name__ == '__main__':
    unittest.main()
