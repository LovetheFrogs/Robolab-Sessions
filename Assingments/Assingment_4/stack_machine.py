#!/usr/bin/env python3
from enum import IntEnum, Enum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class Word(IntEnum):
    """
    Used to check if a codeword is an instruction, an operand or a character
    """
    OPERAND = 0
    INSTRUCTION = 1
    CHARACTER = 2


class Character(Enum):
    """
    Used to check the codeword if it is a character
    """
    NOP = 0b100000
    SPEAK = 0b100001
    SPACE = 0b100010
    NOP1 = 0b100011
    A = 0b100100
    B = 0b100101
    C = 0b100110
    D = 0b100111
    E = 0b101000
    F = 0b101001
    G = 0b101010
    H = 0b101011
    I = 0b101100
    J = 0b101101
    K = 0b101110
    L = 0b101111
    M = 0b110000
    N = 0b110001
    O = 0b110010
    P = 0b110011
    Q = 0b110100
    R = 0b110101
    S = 0b110110
    T = 0b110111
    U = 0b111000
    V = 0b111001
    W = 0b111010
    X = 0b111011
    Y = 0b111100
    Z = 0b111101
    NOP2 = 0b111110
    NOP3 = 0b111111


class Instruction(Enum):
    """
    Used to check the instruction to perform
    """
    STP = 0b010000
    DUP = 0b010001
    DEL = 0b010010
    SWP = 0b010011
    ADD = 0b010100
    SUB = 0b010101
    MUL = 0b010110
    DIV = 0b010111
    EXP = 0b011000
    MOD = 0b011001
    SHL = 0b011010
    SHR = 0b011011
    HEX = 0b011100
    FAC = 0b011101
    NOT = 0b011110
    XOR = 0b011111


def define(code_word: Tuple[int, ...]) -> Word:
    """
    Auxiliary method used to check what a given codeword is
    """
    code_word = list(code_word)
    if code_word[0] == 0 and code_word[1] == 0:
        return Word.OPERAND
    elif code_word[0] != 1:
        return Word.INSTRUCTION
    else:
        return Word.CHARACTER


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        code_word_type = define(code_word)
        if code_word_type == Word.OPERAND:
            num = "".join(str(c) for c in list(code_word)[2:])
            a = int(num, 2)
            self.stack.append(c_ubyte(a))
            self.overflow = False
            return SMState.RUNNING
        code_word = "".join(str(c) for c in list(code_word))
        if code_word_type == Word.CHARACTER:
            self.character(code_word)
        else:
            return self.action(list(code_word))

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """
        if not self.stack:
            return None

        top = self.stack[len(self.stack) - 1]
        if isinstance(top, c_ubyte):
            aux = str(bin(top.value))[2:]
            bin_rep = []
            for i in range(8 - len(aux)):
                bin_rep.append(0)
            for i in aux:
                bin_rep.append(int(i))
            return tuple(bin_rep)
        else:
            return top

    def character(self, code_word: str) -> SMState:
        """
        Operates accordingly if the code_word is a character

        Args:
            code_word (str): Command for the stack machine to execute, parsed into a String
        Returns:
            SMState: Current state of the stack machine
        """
        aux = Character(int(code_word, 2))
        if aux == Character.SPEAK:
            return self.speak()
        elif aux == (Character.NOP or Character.NOP1 or Character.NOP2 or Character.NOP3):
            return SMState.RUNNING
        else:
            try:
                self.stack.append(str(Character(int(code_word, 2)).name))
                self.overflow = False
            except ValueError:
                return SMState.ERROR

    def action(self, code_word: List) -> SMState:
        """
        Performs the instruction referred to by the code word

        Args:
            code_word (List): Command for the stack machine to execute, parsed into a List
        Returns:
            SMState: Current state of the stack machine
        """
        num = int("".join(c for c in list(code_word)), 2)
        action = Instruction(num)
        match action:
            case Instruction.STP:
                return SMState.STOPPED
            case Instruction.DUP:
                return self.duplicate()
            case Instruction.DEL:
                return self.delete()
            case Instruction.SWP:
                return self.swap()
            case Instruction.ADD:
                return self.add()
            case Instruction.SUB:
                return self.subtract()
            case Instruction.MUL:
                return self.multiply()
            case Instruction.DIV:
                return self.divide()
            case Instruction.EXP:
                return self.exponential()
            case Instruction.MOD:
                return self.modulus()
            case Instruction.SHL:
                return self.shift(True)
            case Instruction.SHR:
                return self.shift(False)
            case Instruction.HEX:
                return self.hexadecimal()
            case Instruction.FAC:
                return self.factorial()
            case Instruction.NOT:
                return self.negate()
            case Instruction.XOR:
                return self.xor()

    """ The following functions are each used to execute one instruction """
    def speak(self) -> SMState:
        if not self.stack:
            return SMState.STOPPED
        top = self.stack.pop().value
        if len(self.stack) < top:
            return SMState.STOPPED
        tts = ""
        for _ in range(top):
            aux = self.stack.pop()
            if not isinstance(aux, str):
                tts += str(aux.value)
            elif aux == "SPACE":
                tts += ' '
            else:
                tts += aux
        print(tts)
        return SMState.RUNNING

    def duplicate(self) -> SMState:
        if not self.stack:
            return SMState.STOPPED
        top = self.stack.pop()
        self.stack.append(top)
        self.stack.append(top)
        return SMState.RUNNING

    def delete(self) -> SMState:
        if not self.stack:
            return SMState.STOPPED
        self.stack.pop()
        return SMState.RUNNING

    def swap(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        first = self.stack.pop()
        second = self.stack.pop()
        self.stack.append(first)
        self.stack.append(second)
        return SMState.RUNNING

    def add(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        a = self.stack.pop().value
        b = self.stack.pop().value
        result = a + b
        if result > 255:
            self.overflow = True
            self.stack.append(c_ubyte(255))
        else:
            self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def subtract(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        b = self.stack.pop().value
        a = self.stack.pop().value
        result = a - b
        if 1 << (result.bit_length() - 1):
            self.overflow = True
            self.stack.append(c_ubyte(result))
        else:
            self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def multiply(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        b = self.stack.pop().value
        a = self.stack.pop().value
        result = c_ubyte(a).value * c_ubyte(b).value
        if result > 255:
            self.overflow = True
            self.stack.append(c_ubyte(255))
        else:
            self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def divide(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.ERROR
        b = self.stack.pop().value
        a = self.stack.pop().value
        if b <= 0:
            return SMState.STOPPED
        result = c_ubyte(a).value // c_ubyte(b).value
        self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def exponential(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        b = self.stack.pop().value
        a = self.stack.pop().value
        result = a ** b
        if result > 255:
            self.overflow = True
            self.stack.append(c_ubyte(result))
        else:
            self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def modulus(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        b = self.stack.pop().value
        a = self.stack.pop().value
        result = a % b
        self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def shift(self, direction: bool) -> SMState:
        """
        Shifts the top-most value of the stack to either the right or left

        Args:
            direction (boolean): Determines the direction to shift the value,
             true being shift left and false shift right
        Returns:
             SMState: Current state of the stack machine
        """
        if len(self.stack) < 2:
            return SMState.STOPPED
        b = self.stack.pop().value
        a = self.stack.pop().value
        if direction:
            result = a << b
            if result > 255:
                self.overflow = True
                self.stack.append(c_ubyte(result))
                return SMState.RUNNING
        else:
            result = a >> b
        self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def hexadecimal(self) -> SMState:
        if len(self.stack) < 2:
            return SMState.STOPPED
        valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        a = self.stack.pop()
        b = self.stack.pop()
        if isinstance(a, c_ubyte):
            a = str(a.value)
        if isinstance(b, c_ubyte):
            b = str(b.value)
        if a not in valid or b not in valid:
            return SMState.ERROR
        self.stack.append(c_ubyte(int(a + b, 16)))
        return SMState.RUNNING

    def factorial(self) -> SMState:
        if not self.stack:
            return SMState.STOPPED
        a = self.stack.pop().value
        result = 1
        for i in range(1, a + 1):
            result *= i
        if result > 255:
            self.overflow = True
            self.stack.append(c_ubyte(255))
        else:
            self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def negate(self):
        """
        This comment serves as an explanation for how the result is obtained.
        First - gets the top-most value from the stack as a 4 bit binary number, and represents it as a String
        Second - creates a list of integers where each n position is the nth-bit of the String
        Third - Negates each term of the list and creates a new list
        Fourth - Transforms the integer list into a String by using map()
        Fifth - Transforms the String into an integer
        """
        if not self.stack:
            return SMState.STOPPED
        result = int(''.join(map(str, [
            1 if b == 0 else 0 for b in [int(b) for b in format(self.stack.pop().value, '08b')]
        ])), 2)
        self.stack.append(c_ubyte(result))
        return SMState.RUNNING

    def xor(self) -> SMState:
        """
        This comment serves as an explanation for how the result is obtained
        First - transforms the 2 top-most values from the stack into a 4 bit binary number,
        and represents them as Strings
        Second - transforms each String into a list of integers
        Third - uses the zip() built-in to iterate through each value of each List simultaneously
        Fourth - Creates a new List by performing the XOR oof each pair of bits
        Fifth - Transforms the new integer List into a String using map()
        Sixth - Transforms the String into an integer
        """
        if not self.stack:
            return SMState.STOPPED
        result = int(''.join(map(str, [
            a ^ b for a, b in zip(
                [int(b) for b in format(self.stack.pop().value, '08b')],
                [int(b) for b in format(self.stack.pop().value, '08b')]
            )
        ])), 2)
        self.stack.append(c_ubyte(result))
        return SMState.RUNNING
