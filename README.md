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
PLEASE NOTE THAT THIS IS INCOMPLETE AND ONLY WHAT I NEEDED TO FINISH THE PROJECT=
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
# push
@seg     // Segmetn we push
D=M      // Setting D to M 

@SP
M=M+1   // increment SP; point to new (after command) top of stack
A=M-1   // A=RAM[SP--]
M=D     // push value of register segment_base_addr+index onto stack; RAM[*SP--]=RAM[base_addr+index]

```

```aiignore
# push
```

```aiignore
# pop
@SP     // Addresses stack pointer
AM=M-1  // Decrements stack pointer and update A to new value
D=M     // Pop top of stack into D

@seg    // The segment we're using
M=D     // Setting M to equal D
```
# Specifications of the VM
Booting the VM

1. VM programming function
    - One file in any VM program is expected to be named Main.vm
	- One VM function in this file is expected to be named main()
	
2. When the VM starts running, or is reset
    - Starts executing an argument-less OS function called sys.init
	- Sys.init then calls Main.vm, and enters an infinite loop.
	
3. Bootstrap code
    - Code should be written in assembly
	- Put into the Hack ROM, beginning with Address 0.

	Set SP=256
	Call sys.init
	
	
4. Standard mapping of VM and host RAM on the Hack platform
HACK Ram
0-15 -> Pointers and registers
16-255 -> Static variables
256-2047 -> stack
2048-16383 -> heap
16384-24576 -> memory mapped I/O (everything except keyboard on 24576 is screen)
24577-32767 -> unused memory space

5. Special symbols in VM programs
SP -> points to memory address within host RAM 1 past the top of the stack
LCL,ARG,THIS,THAT -> base addresses within host RAM of the virtual segments local, argument, this, and that
R13-R15 -> Can be used for any purpose
xxx.i -> static variable in xxx.vm file is translated into xxx.j where j is incremented each time a new static variable is encountered
functionName$label
functionName
functionName$ret.i 

5. Handles multiple VM files, a full directory, but generates a single assembly file that contains the sequence of all the functions we're translating.

Main fileName - name of a single source file, or
directoryName - name of a directory containing one more more .vm source files

## Call, Function, Return

### Function

Defines the code to set up / execute a function in assembly

```aiignore
Pseudocode
function SimpleFunction.test 2
(functionName)            // Injects a function entry label into the code
    repeat nVar times:    // nVars = number of local variables
    push 0                // Initializes variables to 0
```

```aiignore
function (functionName)
@arg2       // Sets addressing register for constant, which is arg2(number of args)
D=A         // Sets D register to the value at A
(init_lcl_x)
@SP         // Sets A to SP
AM=M+1      // Increments A and M both by 1
A=A-1       // Decrements the addressing register by 1, but keeps the M value the same
M=0         // Initializes variable, sets it to 0.
@init_lcl_x
D=D-1;JGT   // Subtract 1 from D;jump if D>0            
```

### Return

```aiignore
Pseudocode
endFrame = LCL             // gets the address at frame end
retAddr = *(endFrame -5)   // gets return address
*ARG = pop()               // puts the return value for caller
SP=ARG+1                   // Reposition SP
THAT = *(endFrame - 1)     // restores THAT
THIS = *(endFrame - 2)     // restores THIS
ARG = *(endFrame - 3)      // restores ARG
LCL = *(endFrame - 4)      // restores LCL
goto retAddr               // jumps to return address
```

```aiignore
# get address at frame end
@LCL      // get address at frame end
D=M       // Place @LCL into RAM
@R13      // Here's where we'll put the frame.
M=D       // Place LCL into R13 to operate on

# gets return address
@5        
A=D-A     // Calculates Frame-5
D=M       // Places return address into D.

# puts the return value for caller

@R14       
M=D       // Places return address into R14
@SP       
A=M-1     // Sets address to top of stack
D=M       // Grab the return value

# Repositions stack pointer
@ARG
A=M       // Places the value at ARG into M
M=D       // RAM[ARG] = return value
@ARG
D=M       // Place return value into RAM where ARG was.
@SP
M=D+1     // Places D+1 into RAM at current stack pointer address.

# restores THAT
@R13      // Frame
M=M-1     // Frame-1
A=M       // Move M into the addressing register, so we're working at the frame address
D=M       // Puts Frame-1 into the data register
@THAT
M=D       // Puts D into the Memory register, restoring THAT

# restores THIS
@R13      // Frame-1
M=M-1     // Frame-2
A=M       // Move M into the addressing register, so we're working at the frame address
D=M       // Puts Frame-1 into the data register
@THIS
M=D       // Puts D into the Memory register, restoring THIS

# restores ARG
@R13      // Frame-2
M=M-1     // Frame-3
A=M       // Move M into the addressing register, so we're working at the frame address
D=M       // Puts Frame-1 into the data register
@ARG
M=D       // Puts D into the Memory register, restoring ARG

# restores LCL
@R13      // Frame-3
M=M-1     // Frame-4
A=M       // Move M into the addressing register, so we're working at the frame address
D=M       // Puts Frame-1 into the data register
@LCL
M=D       // Puts D into the Memory register, restoring LCL
```

### Call

Calls function, informs number of nArgs that were pushed to the stack before the call.

#### Pseudocode and assembly
```aiignore
# This is the function frame 
push returnAddress      // Generates label and pushes it to the stack
push LCL                // saves LCL of the caller
push ARG                // saves ARG of the caller
push THIS               // saves THIS of the caller
push THAT               // saves THAT of the caller
# Where the return address should be
ARG = SP-5-nArgs        // repositions ARG to top of arguments
LCL = SP                // repositions LCL to stack pointer
goto function           // transfers control to callee
(returnAddress)         // injects return label into the code
```

```aiignore
# First thing is we push a label, so 
@functionName$ret.X    // Set return label
D=A                    // Put that address into D
@SP                    // Address stack pointer
AM=M+1                 // Push
A=A-1
M=D


```