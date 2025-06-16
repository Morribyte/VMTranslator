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
A=M-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
```

### Pop
* Pops a value from the stack and decrements the stack pointer by 1.
```aiignore
@SP        // Addresses the stack pointer (R0, default 256)
AM=M-1     // Decrements Stack Pointer and updates A to new value.
A=M-1   
```

### add
* Adds two values together
```aiignore
@SP        // Addresses stack pointer
AM=M-1     // Decrements Stack Pointer and update A to new value.
D=M        // Sets D to the second value in the computation.
A=A-1      // Load address below the top of the stack into the A register
M
```
## Segments
### Constant
* Sets a value to a constant number using the A address.
```aiignore
@X         // Load constant "X" into A
D=A        // Move constant into D for storage
```

### Pseudocode and full translation examples
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
A=M-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
# push constant 8
@8         // Load constant 8 into A
D=A        // Move constant into D for storage
@SP        // Addresses the stack pointer (R0, default 256)
AM=M+1     // Increments Stack Pointer and update A to new value.
A=M-1      // Moves A to the top of the stack (SP-1)
M=D        // Store D at the top of the stack
# add
@SP        // Addresses stack pointer
AM=M-1     // Decrements Stack Pointer and update A to new value.
D=M        // Sets D to the second value in the computation.
A=A-1      // Load address below the top of the stack into the A register
M=D+M      // We finally compute and store the value into the top of the stack, but keep our pointer 1 above the stack
```