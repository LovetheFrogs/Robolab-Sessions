# Robolab-Sessions

This repo contains all the Robolab Sessions assingments for winter semester 2023/2024 of TU Dresden.

1. [1st Assingment](#first-assingment)
2. [2nd Assingment](#second-assingment)
3. [3rd Assingment](#third-assingment)
4. [4th Assingment](#fourth-assingment)
5. [Final Assingment](#final-assingment)

## First assingment

The first assignment will help you to understand how Hamming Codes work and how to convert the matrices.
Thus, we will have a deeper look onto the extended Hamming Code $`(8, 4)`$.
The code is capable of detecting a single-bit error and correct it and, by using an additional (overall) parity bit, it can detect (but not to correct) double-bit errors.

### Task 1

Create the non-systematic generator matrix $`G'_{4,8}`$ and the parity-check matrix $`H'_{4,8}`$. Follow the rules for optimal codes from the [Hamming Code specifications](https://robolab.inf.tu-dresden.de/autumn/task/basics_hamming_code/#_construction)

1. Construct $`G'`$ by adding the binary representation in the correct order (SEC-DED).

2. Each binary representation should have exactly $k$ bits with the least significant bit (LSB) at the bottom. Mark the columns containing the parity bits with $`p_1 ... p_r`$ and the data bits with $`d_1 ... d_k`$.

3. Derive $`H'`$ form $`G'`$ considering the order of the data and parity bits. Take into account that you need the transpose of the corresponding row bits from $`G'`$. If not already done extend $`H'`$ to match the matrix definition $`H'_{4,8}`$. Mark the columns holding the parity bits with $`p_1 ... p_r`$ and the data bits with $`d_1 ... d_k`$.

### Task 2

Create the systematic generator matrix $`G_{4,8}`$ and the parity-check matrix $`H_{4,8}`$.
Use your previously generated $`G'_{4,8}`$ as start matrix.

1. Convert $`G'`$ into standard form (RREF) using **row-reduction** only.

2. For each row, write down the calculation steps necessary for the conversion. Write down the resulting matrix after each row processed.

3. Derive $H$ from $G$. For both matrices, mark the columns holding the parity bits with $`p_1 ... p_r`$ and the data bits with $`d_1 ... d_k`$.

### Task 3

Encode the following words $\bar a$ using the non-systematic generator matrix $`G'_{4,8}`$ created in Task 1:

1. $\bar a = (0100)$
2. $\bar a = (1001)$
3. $\bar a = (0011)$
4. $\bar a = (1101)$

Since we use a SEC-DED code, the increased error detection capabilities are achieved by adding an overall parity bit that is calculated upon all $n$ bits of the encoded word. You can check your result against the [parity table](https://robolab.inf.tu-dresden.de/autumn/task/basics_hamming_code/#parity-table) to see, if the values match for $p_4$ at the corresponding position.

### Task 4

Decode the following words $\bar x$ using the systematic parity-check matrix $`H_{4,8}`$ created in Task 2:

1. $\bar x = (11001101)$
2. $\bar x = (10011001)$
3. $\bar x = (11011011)$
4. $\bar x = (11010101)$

Were these words transmitted successfully? If this is not the case, write down the number of detected errors and attempt to correct them.
You can follow these steps:

1. Check if the overall parity bit $p_4$ is correct.

2. Calculate the syndrome vector $\bar z$ and write down the matching pattern. Use the overall parity bit and the syndrome to check for errors following the [error pattern](https://robolab.inf.tu-dresden.de/autumn/task/basics_hamming_code/#error-pattern) table.

3. Correct errors if possible and write down the original (source) word.
Take into account that this might not be possible in some cases.

## Second assingment

In this assignment you’ll have to implement a customized systematic Hamming Code $(10, 6)$ with additional parity bit. The implementation has to be capable of encoding and decoding input words, detecting errors and correcting single-bit errors if they occur. Also, the implementation has to be done in Python using the template provided in ``./hamming_code.py`. You will implement and run the program on your computer.

### Generator matrix

Use the following non-systematic generator matrix $G'_{6,10}$ for your implementation:

$$
G' = 
\begin{bmatrix}
1 & 1 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 \\
1 & 0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 1 & 1 & 0 & 0 \\
1 & 1 & 0 & 1 & 0 & 0 & 0 & 1 & 1 & 0 \\
1 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 1
\end{bmatrix}
$$

### Task 1

Make yourself familiar with the project structure and classes, then do the following steps:

1. Add above matrix $G'_{6,10}$ to your class `HammingCode`.

2. Bring $G'_{6,10}$ into the systematic form through implementing and executing the transformation steps listed [here](https://robolab.inf.tu-dresden.de/autumn/task/hamming_code/#_transformation). Use the pre-defined method **__convert_to_g()** for your implementation.

3. Derive $H_{4,10}$ from the generated matrix $G_{6,10}$. Use the pre-defined method **__derive_h()** for your implementation.

### Task 2

Implement the encoder in the function **encode()** in `./hamming:code.py`:

1. Add the missing logic for encoding given input words. Do not overwrite the existing signature of the method (tests depend on that).

2. Don’t forget to calculate and add the additional parity bit $p_5$ using even parity.

3. Make sure to return the final code as a `Tuple` and not as a `List`.

4. Test your implementation with unit-tests (see Task 4).

### Task 3

Implement the decoder function **decode()** in `./hamming_code.py`:

1. Add the missing logic for decoding given input words. Do not overwrite the existing signature of the method (tests depend on that). Calculate the additional parity bit of the encoded word using even parity. Calculate the syndrome vector without including $p_5$ (separate it beforehand). Check the syndrome vector against $H_{4,10}$ and conclude if the encoded word had an error. 
    - If the encoded word was without an error, return the decoded word and VALID.
    - If the encoded word had a single error, return the corrected decoded word and CORRECTED.
    - If the encoded word had multiple errors, return None and UNCORRECTABLE.

2. Make sure to return the final code as a `Tuple` and not as a `List`.

3. Test your implementation with unit-tests (see Task 4).

### Task 4

Now we are looking into unit-tests and update the file `./test_hamming_code.py`.

1. First, import the subclasses needed from `hamming_code.py`.
2. For every given test case, implement the corresponding logic. Use asserts and pre-defined expectations (e.g. simple variable holding the value) for the checks.
3. Encode the following codes (you can check them in a single function):
    1. $(0, 1, 1, 0, 1, 1)$
    2. $(0, 0, 0, 0, 0, 0)$
    3. $(1, 0, 1, 1, 0, 1)$
    4. $(1, 1, 1, 1, 1, 0)$
4. Decode the following codes:
    1. $(0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0)$
    2. $(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)$
    3. $(1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)$
    4. $(1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1)$
5. Analyze the output. Does the output of *decode()* match the input of *encode()* before?
6. Bring up at least two more test cases (one for codes being corrected and one for an uncorrectable code).

## Third assingment

The third assignment will give you a better understanding of simple stack and register machines and how to perform basic arithmetic operations on them.
For this, we will have a look at the Reverse Polish Notation (RPN) and simulate a stack machine using RPN for the operations.

### Task 1

Do some research on register and stack machines and answer the following questions afterwards:

1. One drawback of stack machines is the need of more memory references. For a simple `ADD` operation of two integers, how many times the data cache is referenced? Write down the steps for the operation.
2. For stack machines, we have a very compact object code (instruction set and rules) which fits in 6 bit or less. In comparison, register machines need more bits for the same instruction on the arithmetic logic unit (ALU). Explain briefly why this is the case and give an average length needed for instructions for register machines.
3. Explain briefly how register and stack machines handle interrupts and why stack machines may have an advantage here.

### Task 2

Make yourself familiar with the Reverse Polish Notation (RPN).

Transform the following mathematical expressions into RPN.
Do not pre-calculate sub-expressions, keep the original operands.
Also, **use only basic arithmetic** here (`ADD`, `SUB`, `MUL`, `DIV`).

1. $4 * (7 + 8 * 9) - 1$
2. $(96 - (4 + 44 * (3 - 1) + 7) * 25)$
3. $(5^3 / (2 + 3)) / 5$

### Task 3

Simulate the execution of the following sequences using our [stack specification](https://robolab.inf.tu-dresden.de/autumn/task/stack_machine/).

1. Transform every instruction and operand into its binary representation beforehand.Set the MSB correctly according to our specification and always end with `STP`.

2. Execute the following sequence:

$$
\begin{matrix}
001010 \\
010001 \\
010001 \\
010110 \\
011111 \\
000100 \\
011011 \\
000100 \\
011001 \\
000110 \\
011000 \\
100010 \\
110110 \\
101000 \\
110101 \\
010000
\end{matrix}
$$

For each binary word do the following:

- If it is an operand or character, push it to the stack.
- If it is an instruction (or character instruction), pop all words needed, executethe instruction, and push the result back to the stack (if there is any).
- Show the current content of the stack (or write down the string).

For both sequences, what is the final content on the stack?

## Fourth assingment

In this assignment you’ll have to implement a (non-real-world) simple stack machine that can perform basic arithmetic operations. The implementation has to be in Python using the template provided in `./stack_machine.py`. Again, you will implement and run the program on your computer.

Read about the specification of our stack machine here: [Specification](https://robolab.inf.tu-dresden.de/autumn/task/stack_machine/).

### Task 1

Implement the function **top()** in `./stack_machine.py`:

1. Implement or define a LIFO stack that holds unsigned 8-bit integers and characters.
2. Add the missing logic to the function top() returning the top element if there is any, or None. Take into account that the items on the stack, depending on the type, probably needs to be converted into a binary tuple beforehand.

### Task 2

Implement the function **do()** in `./stack_machine.py`:

1. Define a representation for stack machine instructions and characters, e.g. using Enums or other classes.
2. Add the missing logic for processing a 6-bit word (a `Tuple`). Handle the input parameter according to our specification. If the word is an operand or a character, push it to the stack. If the word is an instruction or a string operation (e.g. SPEAK), pop the operands needed from the stack and execute the instruction. Don’t forget to push the result back to the stack if there is any.
3. Check for an overflow if required and print the `overflow` state according to our specification.

Stop the execution if there are not enough operands or there was an illegal instruction, e.g. division by 0.

Implement all instructions from our [specification](https://robolab.inf.tu-dresden.de/autumn/task/stack_machine/).

### Task 3

Now we are looking into unit-tests again and update the file `./test_stack_machine.py`.

1. First, import everything from `stack_machine.py`.
2. Implement the instance test case for `StackMachine` as you did for `HammingCode`.
3. Write a test case for the function **top()**. Make sure that the value returned matches our definition (8-bit tuple).

### Task 4

In your file `./src/test_stack_machine.py`, create a test case for the function `do()` and add a check for the final result on the stack. Use asserts and pre-defined expectations (e.g. simple variable holding the value) for the check.

1. Implement and execute the following sequence (taken from assignment 3 and extended). For the `SPEAK` instruction, we only print the output instead of using TTS in this assignment.

$$
\begin{matrix}
001010 \\
010001 \\
010001 \\
010110 \\
011111 \\
000100 \\
011011 \\
000100 \\
011001 \\
000110 \\
011000 \\
100010 \\
110110 \\
101000 \\
110101 \\
010000
\end{matrix}
$$

2. What happens if there was a division by 0 or if there were not enough operands on the stack?

Cover the correct error handling also with unit-tests.

### Task 5

To make sure your stack machine works fine, provide a test case for every instruction listed in our specification. In order to simplify your test cases you can outsource the object creation into a `setUp` function:

```python
def setUp(self):
    self.sm = StackMachine()
```

**Hint** for catching and checking output in unit-tests: We use mocks!

```python

#!/usr/bin/env python3

# Import both io and mock classes
import io
import unittest.mock

...

    # Put this definition before your test function (annotation) and add a parameter
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_func(self, mock_stdout):
        # ...your implementation
        # Access the recorded console output (last item: -1)
        mock_stdout.getvalue()[:-1]
```

## Final Assingment

In this assignment you’ll have to implement the missing parts for your robot and combine it with the other parts implemented earlier. This includes the implementation of a simple analogue-digital-converter for all data the color sensor outputs and the overall mechanics for moving the sensor and scrolling or driving over the bar code cards.

At this point you should already have an idea about how your robot will look in the end and which parts you need in order to solve the upcoming demonstration/exam.

### Basics - How to start

- **The Lego Set / Brick:** Work yourself through the [Getting Started](https://robolab.inf.tu-dresden.de/autumn/getting_started/) instructions (group task). Read the information about our OS and the python libraries to use carefully
- **The Group Repository:** You’ll be given access to a specific repository for this task. Decide intra-group on whose HammingCode implementation and whose StackMachine to use and add the implementation to your group repository. Each group member should provide one of the classes! For the implementation, the entry point is the file `main.py`. So, include all the other files necessary here.

### Task 1 (The Robot)

1. Construct your robot with all parts needed. You’ll need several engines to move the sensor and scroll the bar code cards. Also, you’ll need a light or color sensor for detecting and reading the codeword.
2. Implement the different movement algorithm using the template provided in `./robolab-template/src/robot.py`. Experiment with different speed values for the motors and adjust it to your needs. See the [specifications for the bar code cards](https://robolab.inf.tu-dresden.de/autumn/task/bar_code_cards/#_dimensions) for the overall dimensions and distances between e.g. the bars.

### Task 2 (Hamming Decoder)

1. Implement a routine which reads a line and stores the values received by the sensor in a data structure (e.g. `Tuple`, `List`).
2. Decode the codeword using your class `HammingCode` and stored the opcode received for further processing. Note that, in case the result is **UNCORRECTABLE**, you need to re-read the line and decode it again!
3. Extend your routine with a command to scroll to the next line. You should be able to wait for and scroll to multiple other cards after processing the first one.
4. We want to know what our robot is doing. So, for every codeword do the following (list incomplete):
    - Print (or use TTS) the 11-bit input (e.g. “Input: ( … )”)
    - Print (or use TTS) the 6-bit output (e.g. “Output: ( … )”)
    - Print (or use TTS) exception messages (e.g. input too short, uncorrectable code, …)

### Task 3 (Stack Machine)

1. Extend your logic so that opcodes are handed to the stack machine to be processed. Test your fully implemented robot. Make sure to check the state after each opcode and abort everything if an exception occurs.
2. We want to know what the stack machine is executing. So, for every converted codeword do the following:
    - Print (or use TTS) the instruction shortcut (e.g. “Instruction: XYZ)
    - Print the top element of the stack if it has changed.
    - Print (or use TTS) exception messages (e.g. not enough items, invalid range, …)
