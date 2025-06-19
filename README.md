# VMTranslator
HACK VM Translator

* Create a translator that can handle any VM code and translate it into assembly
* The goal isn't to create a complete reference, rather a document I can use to help myself understand and consistently
  translate commands and build this project.

# Modules
  * Parser
  * Translator (CodeWriter)
  * Main

# Pseudocode and translation guide

Since each part of the code can be expressed as pseudocode then translated into VM code, for every command I'll write
the VM code, some pseudocode then the final assembly code.

There are 8 types of instructions (3 covered right now). We must parse commands to pull our instruction type out.

* C_PUSH
* C_POP 
* C_ARITHMETIC
  * Arithmetic
  * Comparison
  * Logical

1. command
   2. If it's an arithmetic command, it will be just this command
2. Segment
    * Each segment can either be "Direct" or "Indirect" depending on how it's addressed.
    * Constant -> Not a true memory segment, but a virtual one. We take the address from the @ A command and use that
    to assign a constant value.
    * Not used for Arithmetic or return
3. Index
   * Some number
   * Only used for half of the commands. The rest, it's not called.

An instruction will be the same no matter what. What this means in practice is that push will be replaced with the same
set of code, so will add, so will constant, so will local. The only thing that changes is the index.

This means that we should be able to break things down into smaller segments.

* While each VM code line is several commands and numbers strung together, every time we encounter a specific word or number,
  we can be sure what it'll translate into. That is, the same statement will always result in the same code. Therefore, we can
  break each unit of code into an individual set of code and concatenate them together to create the full translation.
  * Check out the [Reference](#Reference) section for individual break down.

# Translation Reference

## Commands
### Push
* Pushes a value onto the stack and increments the stack pointer by 1.
```aiignore
@SP        // Addresses the stack pointer (R0, default 256)
AM=M+1     // Increments Stack Pointer and update A to new value.
A=A-1      // Moves A to the top of the stack (SP-1)
D=M       // Store D at the top of the stack
```

### Pop
* Pops a value from the stack and decrements the stack pointer by 1.
* Since we don't need to save any memory values, we don't need anything other than decrementing the stack pointer.
```aiignore
@SP        // Addresses the stack pointer (R0, default 256)
AM=M-1     // Decrements Stack Pointer and updates A to new value.
D=M        // Places the new memory address (*SP) into RAM[*SP]
```

### add
* Adds two values together
```aiignore
@SP        // Addresses stack pointer
AM=M-1     // Decrements Stack Pointer and update A to new value.
D=M        // Sets D to the second value in the computation.
A=A-1      // Load address below the top of the stack into the A register
M=D+M      // Adds two values
```

### sub
* Subtracts two values
```aiignore
@SP        // Addresses stack pointer
AM=M-1     // Decrements Stack Pointer and update A to new value.
D=M        // Sets D to the second value in the computation.
A=A-1      // Load address below the top of the stack into the A register
M=D-M      // Subtracts two values
```

### eq/lt/gt
* Checks the equality of two values
* If true, sets to -1, which is all bits set to 1
* If false, sets to 0, which is all bits set to 0
```aiignore
A=A-1     // After the first pop, we need to pop a second value.
D=M-D     // Checks if M and D are equal via a subtraction operation.
M=-1      // Setting M to -1 to set for truth
@EQ.#     // Label for jumping and skipping commands. Name EQ/LT/GT 
D;JEQ     // if D==0 then x==y; skip to next command
@SP       // Move to stack pointer
A=M-1     // Select the top of the stack
M=0       // If D!=0, then x!=y
(EQ.#)    // The command to take if we skip.  Name EQ/LT/GT 

```
## Segments
### Constant

* Sets a value to a constant number using the A address.
```aiignore
@X         // Load constant "X" into A
D=A        // Move constant into D for storage
```

#### Pseudocode and full translation examples
* push constant 7
```aiignore

pseudocode:
RAM[SP] = 7             // RAM[256] = 7
SP++                    // SP = 257
```

assembly:
# Use the "constant 7" segment
@7         // Load constant 7 into A
D=A        // Move constant into D for storage
# Use the "push" command
@SP        // Addresses the stack pointer (R0, default 256)
AM=M+1     // Increments Stack Pointer and update A to new value.
A=M-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
```
#### Full examples
* Add.asm
```
Pseudocode:
RAM[SP] = 8             // RAM[257] = 8
SP++                    // SP = 258

SP--                    // SP = 257
D = RAM[SP]             // D = 8

SP--                    // SP = 256
RAM[SP] = RAM[SP] + D   // RAM[256] = 7 + 8 (15)
SP++                    // SP = 257
```

```
Full assembly:
# push constant 7
# Use the "constant 7" segment
@7         // Load constant 7 into A
D=A        // Move constant into D for storage
# Use the "push" command
@SP        // Addresses the stack pointer (R0, default 256)
AM=M+1     // Increments Stack Pointer and update A to new value.
A=A-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
# push constant 8
@8         // Load constant 8 into A
D=A        // Move constant into D for storage
@SP        // Addresses the stack pointer (R0, default 256)
AM=M+1     // Increments Stack Pointer and update A to new value.
A=A-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
# add
@SP        // Addresses stack pointer
AM=M-1     // Decrements Stack Pointer and update A to new value.
D=M        // Sets D to the second value in the computation.
A=A-1      // Load address below the top of the stack into the A register
M=D+M      // We finally compute and store the value into the top of the stack, but keep our pointer 1 above the stack

### Local / Argument/ This / That
* locals segment: stored somewhere in the RAM;
* Indirect memory access (through pointers)
* LCL/ARG/THIS/THAT = base address where the local segment is stored

#### Pseudocode and full translation
```aiignore
# pop local i
# Pop handles in 3 stages -> calculate address -> get value -> store to address
addr ← LCL + i
SP--
RAM[addr] ← RAM[SP]
```

```aiignore
# calculates address [local part of the command]
@i      // Addresses segment index at [i]
D=A     // Places current index into D
@LCL    // Addresses R[1], which stores the start of local 
D=D+M   // stores LCL+i into D
@R13    // Addressing a free register for storing the pointer+index
M=D     // Stores D into M

# Decrements stack poitner and pops into D [pop part of the command]
@SP     // Addresses stack pointer
AM=M-1  // Decrements stack pointer and update A to new value
D=M     // Pop top of stack into D

# writes to LCL+i [
@R13    // Addresses to R13
A=M     // Writes LCL+i into A
M=D     // Writes D into M

```

```aiignore
# push local i
addr ← LCL + i
RAM[SP] ← RAM[addr]
SP++
```
@i      // Address segment index at [i]
D=A     // Pushes A into the data register
@LCL    // Addresses the LCL segment
A=D+M   // Adds i to LCL
D=M     // Store RAM[base_addr+index]
@SP     // Address the stackpointer
AM=M+1  // Increments stack pointer and update A to new value
A=A-1   // Moves at to the top of the stack (SP-1)
D=M     // push value of register segment_base+base_addr onto stack.

### Temp / Pointer / Static
* Mapped to RAM[5-12].
* Direct memory access
* RAM[5+i] 
#### Pseudocode and full translation
```aiignore
# push temp i
@i       // Addressing i
D=A      // Setting D to equal A 
@lbl     // Our label
A=D+M    // Addressing D+i
D=M      // setting the D to M.

@SP
M=M+1   // increment SP; point to new (after command) top of stack
A=M-1   // A=RAM[SP--]
M=D     // push value of register segment_base_addr+index onto stack; RAM[*SP--]=RAM[base_addr+index]

```

```aiignore
# pop temp i
@SP     // Addresses stack pointer
AM=M-1  // Decrements stack pointer and update A to new value
D=M     // Pop top of stack into D

@seg    // The segment we're using
M=D     // Setting M to equal D
```

