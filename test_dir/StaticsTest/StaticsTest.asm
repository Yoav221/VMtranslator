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
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// Save return address
// call Class1.set 2
@Class1.set$ret.1
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
@2
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
@Class1.set
0;JMP
(Class1.set$ret.1)
@SP
AM=M-1
D=M
@5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// Save return address
// call Class2.set 2
@Class2.set$ret.2
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
@2
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
@Class2.set
0;JMP
(Class2.set$ret.2)
@SP
AM=M-1
D=M
@5
M=D
// Save return address
// call Class1.get 0
@Class1.get$ret.3
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
@Class1.get
0;JMP
(Class1.get$ret.3)
// Save return address
// call Class2.get 0
@Class2.get$ret.4
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
@Class2.get
0;JMP
(Class2.get$ret.4)
(END)
@END
0;JMP

// Translating file: Class1
(Class1.set)
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
@SP
AM=M-1
D=M
@Class1.0
M=D
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class1.1
M=D
@0
D=A
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
(Class1.get)
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class1.1
D=M
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

// Translating file: Class2
(Class2.set)
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
@SP
AM=M-1
D=M
@Class2.0
M=D
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class2.1
M=D
@0
D=A
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
(Class2.get)
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class2.1
D=M
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
