from parser import Parser, C_POP, C_PUSH, C_ARITHMETIC
from code_writer import CodeWriter

class VMTranslator:

    def __init__(self, input_file):
        self.parser = Parser(input_file)  # Initialize with input file
        self.output_file = input_file.replace(".vm", ".asm")
        self.code_writer = CodeWriter(self.output_file)

    def translate(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            command_type = self.parser.command_type()

            if command_type == C_ARITHMETIC:
                command = self.parser.arg1()
                self.code_writer.writeArithmetic(command)

            elif command_type in ["C_PUSH", "C_POP"]:
                command = "push" if command_type == "C_PUSH" else "pop"
                segment = self.parser.arg1()
                index = self.parser.arg2()
                self.code_writer.writePushPop(command, segment, index)

        self.code_writer.close()



