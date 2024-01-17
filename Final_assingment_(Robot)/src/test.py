#!/usr/bin/env python3

import io
import unittest.mock
from hamming_code import *
from stack_machine import *


class TestRobot(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_example(self, mock_stdout):
        """
            Example implementation of whole workflow:
                - Decode valid/correctable codes and
                - Execute the opcodes on the stack machine
                - Checking the final result afterwards
        """
        hc = HammingCode()
        sm = StackMachine()
        sm.do(hc.decode(tuple([0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]))[0])
        sm.do(hc.decode(tuple([0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]))[0])
        sm.do(hc.decode(tuple([0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]))[0])
        sm.do(hc.decode(tuple([0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0]))[0])
        sm.do(hc.decode(tuple([0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1]))[0])
        sm.do(hc.decode(tuple([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1]))[0])
        sm.do(hc.decode(tuple([0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]))[0])
        sm.do(hc.decode(tuple([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1]))[0])
        sm.do(hc.decode(tuple([0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]))[0])
        sm.do(hc.decode(tuple([0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1]))[0])
        sm.do(hc.decode(tuple([0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1]))[0])
        sm.do(hc.decode(tuple([1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]))[0])
        sm.do(hc.decode(tuple([1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1]))[0])
        sm.do(hc.decode(tuple([1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]))[0])
        sm.do(hc.decode(tuple([1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0]))[0])
        sm.do(hc.decode(tuple([0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]))[0])
        sm.do(hc.decode(tuple([1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]))[0])
        sm.do(hc.decode(tuple([0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]))[0])
        assert mock_stdout.getvalue()[:-1] == "RES 64"


if __name__ == '__main__':
    unittest.main()
