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

## Assingment 3

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
    $001010$
    $010001$
    $010001$
    $010110$
    $011111$
    $000100$
    $011011$
    $000100$
    $011001$
    $000110$
    $011000$
    $100010$
    $110110$
    $101000$
    $110101$
    $010000$

For each binary word do the following:

- If it is an operand or character, push it to the stack.
- If it is an instruction (or character instruction), pop all words needed, executethe instruction, and push the result back to the stack (if there is any).
- Show the current content of the stack (or write down the string).

For both sequences, what is the final content on the stack?
