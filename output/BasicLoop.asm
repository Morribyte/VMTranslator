// Translated VM File @ output/BasicLoop.asm
// push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// pop local 0
@0
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// label LOOP
($LOOP)
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
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// pop local 0
@0
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
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
// push constant 1
@1
D=A
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
// pop argument 0
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
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
// if-goto LOOP
@SP
AM=M-1
D=M
@$LOOP
D;JNE
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
