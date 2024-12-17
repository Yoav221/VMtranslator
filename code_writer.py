class CodeWriter:
    def __init__(self, output_path):
        self.output_path = output_path
        self.output_file = open(self.output_path, 'w')
        self.label_counter = 0  # For unique labels in comparison operations
        self.call_counter = 0 # For unique function calls

    def write_lines(self, lines):
        for line in lines:
            self.output_file.write(line + '\n')

    def close(self):
        self.output_file.close()

    def writeArithmetic(self, command):
        """Writes assembly code for arithmetic-logical VM command"""
        if command == "add":
            # Pop two values and add them
            self.write_lines([
                "@SP",  # Get stack pointer
                "AM=M-1",  # Decrement SP and get address
                "D=M",  # D = y
                "A=A-1",  # Point to x
                "M=D+M"  # x + y
            ])

        elif command == "sub":
            # Pop two values and subtract
            self.write_lines([
                "@SP",  # Get stack pointer
                "AM=M-1",  # Decrement SP and get address
                "D=M",  # D = y
                "A=A-1",  # Point to x
                "M=M-D"  # x - y
            ])

        elif command == "neg":
            # Negate top value
            self.write_lines([
                "@SP",  # Get stack pointer
                "A=M-1",  # Point to top of stack
                "M=-M"  # Negate value
            ])

        elif command in ["eq", "gt", "lt"]:
            # Compare top two values
            label_true = f"{command}_true_{self.label_counter}"
            label_end = f"{command}_end_{self.label_counter}"
            self.label_counter += 1

            comparison = {
                "eq": "JEQ",
                "gt": "JGT",
                "lt": "JLT"
            }[command]

            self.write_lines([
                "@SP",  # Get stack pointer
                "AM=M-1",  # Decrement SP and get address
                "D=M",  # D = y
                "A=A-1",  # Point to x
                "D=M-D",  # D = x - y
                f"@{label_true}",
                f"D;{comparison}",  # Jump if comparison true
                "@SP",  # False case
                "A=M-1",
                "M=0",  # Push false (0)
                f"@{label_end}",
                "0;JMP",  # Skip true case
                f"({label_true})",
                "@SP",  # True case
                "A=M-1",
                "M=-1",  # Push true (-1)
                f"({label_end})"
            ])

        elif command == "and":
            self.write_lines([
                "@SP",  # Get stack pointer
                "AM=M-1",  # Decrement SP and get address
                "D=M",  # D = y
                "A=A-1",  # Point to x
                "M=D&M"  # x AND y
            ])

        elif command == "or":
            self.write_lines([
                "@SP",  # Get stack pointer
                "AM=M-1",  # Decrement SP and get address
                "D=M",  # D = y
                "A=A-1",  # Point to x
                "M=D|M"  # x OR y
            ])

        elif command == "not":
            self.write_lines([
                "@SP",  # Get stack pointer
                "A=M-1",  # Point to top of stack
                "M=!M"  # NOT x
            ])

    def writePushPop(self, command, segment, index):
        """Writes assembly code for push/pop VM command"""
        # Dictionary mapping segments to their base registers
        segment_table = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "5",  # temp starts at R5
            "pointer": "3"  # pointer starts at R3
        }

        if command == "push":  # Handle push command
            if segment == "constant":
                # Push constant value
                self.write_lines([
                    f"@{index}",  # Load constant into A
                    "D=A",  # D = constant
                    "@SP",  # Get stack pointer
                    "A=M",  # Go to address of stack pointer
                    "M=D",  # Write D to top of stack
                    "@SP",  # Get stack pointer again
                    "M=M+1"  # Increment SP
                ])

            elif segment in ["local", "argument", "this", "that"]:
                # Push from segment[index]
                self.write_lines([
                    f"@{segment_table[segment]}",  # Load base address
                    "D=M",  # D = base
                    f"@{index}",  # Load index
                    "A=D+A",  # A = base + index
                    "D=M",  # D = RAM[base + index]
                    "@SP",  # Load SP
                    "A=M",  # A = SP address
                    "M=D",  # Push D to stack
                    "@SP",
                    "M=M+1"  # SP++
                ])

            elif segment == "temp" or segment == "pointer":
                # Push from temp/pointer (direct addressing)
                base = int(segment_table[segment])
                self.write_lines([
                    f"@{base + index}",  # Get direct address
                    "D=M",  # D = value at address
                    "@SP",  # Load SP
                    "A=M",  # A = SP address
                    "M=D",  # Push to stack
                    "@SP",
                    "M=M+1"  # SP++
                ])

            elif segment == "static":
                # Push from static variable
                self.write_lines([
                    f"@{self.filename}.{index}",  # Load static variable
                    "D=M",  # D = value
                    "@SP",  # Load SP
                    "A=M",  # A = SP address
                    "M=D",  # Push to stack
                    "@SP",
                    "M=M+1"  # SP++
                ])

        elif command == "pop":  # Handle pop command
            if segment in ["local", "argument", "this", "that"]:
                # Pop to segment[index]
                self.write_lines([
                    f"@{segment_table[segment]}",  # Load base
                    "D=M",  # D = base
                    f"@{index}",  # Load index
                    "D=D+A",  # D = base + index
                    "@R13",  # Use R13 for temp storage
                    "M=D",  # R13 = base + index
                    "@SP",  # Load SP
                    "AM=M-1",  # SP--, A = SP
                    "D=M",  # D = popped value
                    "@R13",  # Load saved address
                    "A=M",  # A = base + index
                    "M=D"  # RAM[base + index] = D
                ])

            elif segment == "temp" or segment == "pointer":
                # Pop to temp/pointer (direct addressing)
                base = int(segment_table[segment])
                self.write_lines([
                    "@SP",  # Load SP
                    "AM=M-1",  # SP--, A = SP
                    "D=M",  # D = popped value
                    f"@{base + index}",  # Load target address
                    "M=D"  # Store value at address
                ])

            elif segment == "static":
                # Pop to static variable
                self.write_lines([
                    "@SP",  # Load SP
                    "AM=M-1",  # SP--, A = SP
                    "D=M",  # D = popped value
                    f"@{self.filename}.{index}",  # Load static variable
                    "M=D"  # Store value
                ])

    def writeLabel(self, label):
        self.write_lines([f"({label})"])

    def writeGoto(self, label):
        self.write_lines([
            f"@{label}",
            "0;JMP"
        ])

    def writeIf(self, label):
        self.write_lines([
            "@SP",  # A = stack pointer address
            "AM=M-1",  # M[SP] = M[SP]-1, A = M[SP]
            "D=M",  # D = value at top of stack
            "@" + label,  # Load jump destination
            "D;JNE",  # Jump if D ≠ 0 (value is true)
        ])

    def writeFunction(self, functionName, nVars):
        self.write_lines([f"({functionName})"])

        for i in range(nVars):
            self.write_lines([
                "@SP",  # A = address of stack pointer
                "A=M",  # A = value of stack pointer (top of stack)
                "M=0",  # M[SP] = 0 (initialize local var to 0)
                "@SP",  # A = address of stack pointer
                "M=M+1"  # SP++ (increment stack pointer)
            ])

    def writeCall(self, functionName, nArgs):
        return_address = f"{functionName}$ret.{self.call_counter}"
        self.call_counter += 1

        # Save return address
        self.write_lines([
            "// Save return address",
            f"// call {functionName} {nArgs}",
            f"@{return_address}",  # Load return address
            "D=A",
            "@SP",                 # Push it to stack
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ])

        # Push LCL, ARG, THIS, THAT
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.write_lines([
                "//Save the caller's Segments",
                f"@{segment}",  # Load segment
                "D=M",
                "@SP",  # Push it to stack
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ])

        # ARG = SP - nArgs - 5
        self.write_lines([
            "Repositioning Arg for the callee",
            "@SP",
            "D=M",
            f"@{nArgs}",
            "D=D-A",
            "@5",
            "D=D-A",
            "@ARG",
            "M=D"
        ])

        # LCL = SP
        self.write_lines([
            "//LCL = SP",
            "@SP",
            "D=M",
            "@LCL",
            "M=D"
        ])

        # goto functionName
        self.write_lines([
            f"@{functionName}",
            "0;JMP"
        ])

        # (return-address)
        self.write_lines([
            f"({return_address})"
        ])
    def writeReturn(self):
        self.write_lines([
            f"//Store our frame (LCL) in R13 temporally",
            "@LCL",
            "D=M",
            "@R13",
            "M=D"
        ])
        self.write_lines([
            f"// Store return address in R14",
            "@5",
            "D=A",
            "@R13",
            "D=M-D", ##frame (LCL) - 5
            "A=D",
            "D=M", ## D holds the pointer to frame
            "@R14", ## hold the return address
            "M=D"
        ])
        self.write_lines([
            f"// Get return value and store in arg0",
            "@SP",
            "M=M-1",  ##SP --
            "A=M",
            "D=M",  ##D = *SP (return value)
            "@ARG",
            "A=M",  ## D holds the pointer to frame
            "M=D",  ##*ARG = return value
        ])
        self.write_lines([
            f"// Restore SP",
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D" ## SP = ARGS+1
        ])
        self.write_lines([
            f"// Restore THAT",
            "@R13",
            "M=M-1", ##frame (LCL) --
            "A=M",
            "D=M", ## D = pointer to frame-1
            "@THAT",
            "M=D" ## THAT - pointer to frame -1
        ])
        self.write_lines([
            f"// Restore THIS",
            "@R13",
            "M=M-1",  ##frame (LCL) --
            "A=M",
            "D=M",  ## D = pointer to frame-2
            "@THIS",
            "M=D"  ## THIS - pointer to frame -2
        ])
        self.write_lines([
            f"// Restore ARG",
            "@R13",
            "M=M-1",  ##frame (LCL) --
            "A=M",
            "D=M",  ## D = pointer to frame-3
            "@ARG",
            "M=D"  ## ARG - pointer to frame -3
        ])
        self.write_lines([
            f"// Restore LCL",
            "@R13",
            "M=M-1",  ##frame (LCL) --
            "A=M",
            "D=M",  ## D = pointer to frame-4
            "@LCL",
            "M=D"  ## LCL - pointer to frame -4
        ])
        self.write_lines([
            f"// Jump to return address",
            "@R14", ##Storing the location of return address
            "A=M",
            "0;JMP",
        ])






















