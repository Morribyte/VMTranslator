// Translated VM File @ output/input\FibonacciElement\Sys.vm.asm
// function Sys.init 0
@2
D=A
(init_lcl.1)
@SP
AM=M+1
A=A-1
M=0
@init_lcl.1
D=D-1;JGT
// push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D
// call Main.fibonacci 1
@4
D=A
@SP
AM=M+1
A=A-1
M=D
// label END
(END)
// goto END
@END
0;JMP
