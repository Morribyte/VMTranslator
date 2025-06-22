// Translated VM File @ output/SimpleFunction.asm
// function SimpleFunction.test 2
@2
D=A
(init_lcl.0)
@SP
AM=M+1
A=A-1
M=0
@init_lcl.0
D=D-1;JGT
// push local 0
@0
D=A
@LCL
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// push local 1
@1
D=A
@LCL
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// not
@SP
A=M-1
M=!M
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// return
@SP
AM=M-1
D=M
A=A-1
M=M-D
