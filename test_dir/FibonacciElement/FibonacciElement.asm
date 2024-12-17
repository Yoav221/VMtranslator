// Bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
// Save return address
// call Sys.init 0
@Sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// Repositioning Arg for the callee
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
//LCL = SP
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init$ret.0)

// Translating file: Sys
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// Save return address
// call Main.fibonacci 1
@Main.fibonacci$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// Repositioning Arg for the callee
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)
(END)
@END
0;JMP

// Translating file: Main
(Main.fibonacci)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@lt_true_0
D;JLT
@SP
A=M-1
M=0
@lt_end_0
0;JMP
(lt_true_0)
@SP
A=M-1
M=-1
(lt_end_0)
@SP
AM=M-1
D=M
@N_LT_2
D;JNE
@N_GE_2
0;JMP
(N_LT_2)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//Store our frame (LCL) in R13 temporally
@LCL
D=M
@R13
M=D
// Store return address in R14
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// Get return value and store in arg0
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// Restore SP
@ARG
D=M+1
@SP
M=D
// Restore THAT
@R13
M=M-1
A=M
D=M
@THAT
M=D
// Restore THIS
@R13
M=M-1
A=M
D=M
@THIS
M=D
// Restore ARG
@R13
M=M-1
A=M
D=M
@ARG
M=D
// Restore LCL
@R13
M=M-1
A=M
D=M
@LCL
M=D
// Jump to return address
@R14
A=M
0;JMP
(N_GE_2)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
// Save return address
// call Main.fibonacci 1
@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// Repositioning Arg for the callee
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
// Save return address
// call Main.fibonacci 1
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//Save the caller's Segments
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// Repositioning Arg for the callee
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)
@SP
AM=M-1
D=M
A=A-1
M=D+M
//Store our frame (LCL) in R13 temporally
@LCL
D=M
@R13
M=D
// Store return address in R14
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// Get return value and store in arg0
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// Restore SP
@ARG
D=M+1
@SP
M=D
// Restore THAT
@R13
M=M-1
A=M
D=M
@THAT
M=D
// Restore THIS
@R13
M=M-1
A=M
D=M
@THIS
M=D
// Restore ARG
@R13
M=M-1
A=M
D=M
@ARG
M=D
// Restore LCL
@R13
M=M-1
A=M
D=M
@LCL
M=D
// Jump to return address
@R14
A=M
0;JMP
