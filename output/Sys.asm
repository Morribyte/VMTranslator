// Translated VM File @ output/Sys.asm
// function Sys.init 0
@2
D=A
(init_lcl.Sys.init)
@SP
AM=M+1
A=A-1
M=0
D=D-1
@init_lcl.Sys.init
D;JGT
// push constant 4000
@4000
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5000
@5000
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// call Sys.main 0
@SP
AM=M-1
D=M
@THAT
M=D
// pop temp 1
@SP
AM=M-1
D=M
@6
M=D
// label LOOP
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function Sys.main 5
@2
D=A
(init_lcl.Sys.main)
@SP
AM=M+1
A=A-1
M=0
D=D-1
@init_lcl.Sys.main
D;JGT
// push constant 4001
@4001
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5001
@5001
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// push constant 200
@200
D=A
@SP
AM=M+1
A=A-1
M=D
// pop local 1
@1
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
// push constant 40
@40
D=A
@SP
AM=M+1
A=A-1
M=D
// pop local 2
@2
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
// push constant 6
@6
D=A
@SP
AM=M+1
A=A-1
M=D
// pop local 3
@3
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
// push constant 123
@123
D=A
@SP
AM=M+1
A=A-1
M=D
// call Sys.add12 1
@123
D=A
@SP
AM=M+1
A=A-1
M=D
// pop temp 0
@SP
AM=M-1
D=M
@5
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
// push local 2
@2
D=A
@LCL
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// push local 3
@3
D=A
@LCL
A=D+M
D=M
@R13
@SP
AM=M+1
A=A-1
M=D
// push local 4
@4
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
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// return
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
M=M-1
A=M
D=M
@THAT
M=D
@R13
M=M-1
A=M
D=M
@THIS
M=D
@R13
M=M-1
A=M
D=M
@ARG
M=D
@R13
M=M-1
A=M
D=M
@LCL
M=D
// function Sys.add12 0
@2
D=A
(init_lcl.Sys.add12)
@SP
AM=M+1
A=A-1
M=0
D=D-1
@init_lcl.Sys.add12
D;JGT
// push constant 4002
@4002
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5002
@5002
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
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
// push constant 12
@12
D=A
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
// return
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
M=M-1
A=M
D=M
@THAT
M=D
@R13
M=M-1
A=M
D=M
@THIS
M=D
@R13
M=M-1
A=M
D=M
@ARG
M=D
@R13
M=M-1
A=M
D=M
@LCL
M=D
