

class CodeWriter:
    def __init__(self, output_path):
        self.output_path = output_path
        self.output_file = open(self.output_path, 'w')
        self.label_counter = 0  # For unique labels in comparison operations
        self.filename = output_path.split('/')[-1].split('\\')[-1].split('.')[0]


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
