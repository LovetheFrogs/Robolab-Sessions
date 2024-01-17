#!/usr/bin/env python3

import unittest
from stack_machine import *
import io
import unittest.mock


class TestStackMachine(unittest.TestCase):

    def setUp(self):
        """ Creates an instance of a Stack Machine and pushes the values 5 and 2 to the stack """
        self.sm = StackMachine()
        self.sm.do(tuple([0, 0, 0, 1, 0, 1]))
        self.sm.do(tuple([0, 0, 0, 0, 1, 0]))

    def setUp_speak(self):
        """ Creates an instance of a Stack Machine and pushes values to use the SPEAK instruction """
        self.sm = StackMachine()
        self.sm.do(tuple([1, 0, 0, 1, 1, 1]))
        self.sm.do(tuple([1, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([1, 1, 0, 1, 0, 1]))
        self.sm.do(tuple([1, 1, 0, 0, 1, 0]))
        self.sm.do(tuple([1, 1, 1, 0, 1, 0]))
        self.sm.do(tuple([1, 0, 0, 0, 1, 0]))
        self.sm.do(tuple([1, 1, 0, 0, 1, 0]))
        self.sm.do(tuple([1, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([1, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([1, 0, 1, 0, 0, 0]))
        self.sm.do(tuple([1, 0, 1, 0, 1, 1]))
        self.sm.do(tuple([0, 0, 1, 0, 1, 1]))

    def test_instance(self):
        """ Essential: Test class instantiation """
        machine = StackMachine()
        assert machine.overflow is False

    def test_top(self):
        """ Test the return value of the top function """
        machine = StackMachine()
        assert machine.top() is None
        machine.do(tuple([0, 0, 0, 1, 0, 1]))
        assert machine.top() == tuple([0, 0, 0, 0, 0, 1, 0, 1])
        machine.stack.append('s')
        assert machine.top() == 's'

    def test_do(self):
        """ Tests the do function """
        machine = StackMachine()
        machine.do(tuple([0, 0, 1, 0, 1, 0]))
        machine.do(tuple([0, 1, 0, 0, 0, 1]))
        machine.do(tuple([0, 1, 0, 0, 0, 1]))
        machine.do(tuple([0, 1, 0, 1, 1, 0]))
        machine.do(tuple([0, 1, 1, 1, 1, 1]))
        machine.do(tuple([0, 0, 0, 1, 0, 0]))
        machine.do(tuple([0, 1, 1, 0, 1, 1]))
        machine.do(tuple([0, 0, 0, 1, 0, 0]))
        machine.do(tuple([0, 1, 1, 0, 0, 1]))
        machine.do(tuple([0, 0, 0, 1, 1, 0]))
        machine.do(tuple([0, 1, 1, 0, 0, 0]))
        machine.do(tuple([1, 0, 0, 0, 1, 0]))
        machine.do(tuple([1, 1, 0, 1, 1, 0]))
        machine.do(tuple([1, 0, 1, 0, 0, 0]))
        machine.do(tuple([1, 1, 0, 1, 0, 1]))
        machine.do(tuple([0, 0, 0, 1, 0, 1]))
        machine.do(tuple([1, 0, 0, 0, 0, 1]))
        machine.do(tuple([0, 1, 0, 0, 0, 0]))
        assert machine.stack == []

    def test_invalid_stack(self):
        """ Tests what happens if an operation is done without enough operands"""
        machine = StackMachine()
        assert machine.do(tuple([0, 1, 0, 0, 0, 1])) == SMState.STOPPED
        machine.do(tuple([0, 0, 1, 0, 1, 0]))
        assert machine.do(tuple([0, 1, 0, 1, 0, 0])) == SMState.STOPPED

    def test_division_by_zero(self):
        """ Tests what happens if we try to divide by zero """
        machine = StackMachine()
        machine.do(tuple([0, 0, 1, 0, 1, 0]))
        machine.do(tuple([0, 0, 0, 0, 0, 0]))
        assert machine.do(tuple([0, 1, 0, 1, 1, 1])) == SMState.STOPPED

    """ The following tests test each instruction of the Stack Machine """
    def test_stp(self):
        self.setUp()
        assert self.sm.do(tuple([0, 1, 0, 0, 0, 0])) == SMState.STOPPED

    def test_dup(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 0, 0, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 1, 0])

    def test_del(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 0, 1, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 1, 0, 1])

    def test_swp(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 0, 1, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 1, 0, 1])
        self.sm.stack.pop()
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 1, 0])

    def test_add(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 1, 0, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 1, 1, 1])
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 1, 0]))
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 0, 0]))
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 0, 0]))
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 0, 0]))
        assert self.sm.top() == tuple([1, 1, 1, 1, 1, 1, 1, 1])
        assert self.sm.overflow is True

    def test_sub(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 1, 0, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 1, 1])
        self.sm.do(tuple([0, 0, 1, 0, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 0, 1]))
        assert self.sm.top() == tuple([1, 1, 1, 1, 1, 0, 0, 0])
        assert self.sm.overflow is True

    def test_mul(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 1, 1, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 1, 0, 1, 0])
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 1, 0, 1, 1, 0]))
        self.sm.do(tuple([0, 0, 0, 1, 0, 0]))
        self.sm.do(tuple([0, 1, 0, 1, 1, 0]))
        assert self.sm.top() == tuple([1, 1, 1, 1, 1, 1, 1, 1])
        assert self.sm.overflow is True

    def test_div(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 0, 1, 1, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 1, 0])

    def test_exp(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 0, 0, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 1, 1, 0, 0, 1])
        self.sm.do(tuple([0, 0, 1, 1, 1, 1]))
        self.sm.do(tuple([0, 0, 0, 1, 0, 0]))
        self.sm.do(tuple([0, 1, 1, 0, 0, 0]))
        assert self.sm.top() == tuple([1, 1, 0, 0, 0, 0, 0, 1])
        assert self.sm.overflow is True

    def test_mod(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 0, 0, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 0, 1])

    def test_shl(self):
        self.setUp()
        self.sm.do(tuple([0, 0, 1, 1, 0, 1]))
        self.sm.do(tuple([0, 1, 1, 0, 1, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 0, 0])
        assert self.sm.overflow is True
        self.sm.do(tuple([0, 0, 0, 0, 1, 0]))
        self.sm.do(tuple([0, 0, 0, 0, 1, 0]))
        self.sm.do(tuple([0, 1, 1, 0, 1, 0]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 1, 0, 0, 0])

    def test_shr(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 0, 1, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 0, 1])

    def test_hex(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 1, 0, 0]))
        assert self.sm.top() == tuple([0, 0, 1, 0, 0, 1, 0, 1])
        self.sm.do(tuple([1, 0, 0, 1, 0, 1]))
        self.sm.do(tuple([0, 0, 0, 1, 1, 0]))
        self.sm.do(tuple([0, 1, 1, 1, 0, 0]))
        assert self.sm.top() == tuple([0, 1, 1, 0, 1, 0, 1, 1])
        assert self.sm.do(tuple([0, 1, 1, 1, 0, 0])) == SMState.ERROR

    def test_fac(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 1, 0, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 0, 1, 0])
        self.sm.do(tuple([0, 0, 0, 1, 1, 0]))
        self.sm.do(tuple([0, 1, 1, 1, 0, 1]))
        assert self.sm.top() == tuple([1, 1, 1, 1, 1, 1, 1, 1])
        assert self.sm.overflow is True

    def test_not(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 1, 1, 0]))
        assert self.sm.top() == tuple([1, 1, 1, 1, 1, 1, 0, 1])

    def test_xor(self):
        self.setUp()
        self.sm.do(tuple([0, 1, 1, 1, 1, 1]))
        assert self.sm.top() == tuple([0, 0, 0, 0, 0, 1, 1, 1])

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_speak(self, mock_stdout):
        self.setUp_speak()
        self.sm.do(tuple([1, 0, 0, 0, 0, 1]))
        assert mock_stdout.getvalue()[:-1] == "HELLO WORLD"


if __name__ == '__main__':
    unittest.main()
