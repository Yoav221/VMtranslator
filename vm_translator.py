from parser import Parser
from code_writer import CodeWriter
import os
import sys


class VMTranslator:
    def __init__(self, input_path):
        # Remove trailing slash if present
        self.input_path = input_path.rstrip('/')

        if os.path.isdir(self.input_path):
            # Get directory name for output file name
            dir_name = os.path.basename(self.input_path)

            # Find all .vm files in the directory (not in subdirectories)
            self.input_files = [
                os.path.join(self.input_path, f)
                for f in os.listdir(self.input_path)
                if f.endswith('.vm') and os.path.isfile(os.path.join(self.input_path, f))
            ]

            # Create output file with directory name
            self.output_file = os.path.join(self.input_path, f"{dir_name}.asm")
        else:
            # Single file case
            self.input_files = [self.input_path]
            self.output_file = self.input_path.replace('.vm', '.asm')

        if not self.input_files:
            raise ValueError(f"No .vm files found in {self.input_path}")

        self.code_writer = CodeWriter(self.output_file)

        # Write bootstrap code only if Sys.vm exists in directory
        if os.path.isdir(self.input_path):
            sys_vm_exists = any(f.endswith('Sys.vm') for f in self.input_files)
            if sys_vm_exists:
                self.write_bootstrap()

    def write_bootstrap(self):
        """Writes bootstrap code that sets SP=256 and calls Sys.init"""
        self.code_writer.write_lines([
            "// Bootstrap code",
            "@256",
            "D=A",
            "@SP",
            "M=D",  # SP = 256
            "// call Sys.init 0"
        ])
        self.code_writer.writeCall("Sys.init", 0)

    def translate(self):
        """Translates all VM files"""
        # If processing a directory, translate Sys.vm first if it exists
        if os.path.isdir(self.input_path):
            sys_file = next((f for f in self.input_files if f.endswith('Sys.vm')), None)
            if sys_file:
                self.translate_file(sys_file)
                self.input_files.remove(sys_file)

        # Translate remaining files
        for vm_file in self.input_files:
            self.translate_file(vm_file)
        self.code_writer.close()

    def translate_file(self, input_file):
        """Translates a single VM file"""
        # Set filename for static variable handling (removing .vm extension)
        self.code_writer.filename = os.path.basename(input_file).replace('.vm', '')

        # Add comment to mark start of new VM file translation
        self.code_writer.write_lines([f"\n// Translating file: {self.code_writer.filename}"])

        parser = Parser(input_file)

        while parser.hasMoreLines():
            parser.advance()
            if not parser.line:  # Skip empty lines
                continue

            command_type = parser.command_type()

            if command_type == parser.C_ARITHMETIC:
                command = parser.arg1()
                self.code_writer.writeArithmetic(command)

            elif command_type in [parser.C_PUSH, parser.C_POP]:
                command = "push" if command_type == parser.C_PUSH else "pop"
                segment = parser.arg1()
                index = parser.arg2()
                self.code_writer.writePushPop(command, segment, index)

            elif command_type == parser.C_LABEL:
                label = parser.arg1()
                self.code_writer.writeLabel(label)

            elif command_type == parser.C_GOTO:
                label = parser.arg1()
                self.code_writer.writeGoto(label)

            elif command_type == parser.C_IF:
                label = parser.arg1()
                self.code_writer.writeIf(label)

            elif command_type == parser.C_FUNCTION:
                function_name = parser.arg1()
                num_locals = parser.arg2()
                self.code_writer.writeFunction(function_name, num_locals)

            elif command_type == parser.C_RETURN:
                self.code_writer.writeReturn()

            elif command_type == parser.C_CALL:
                function_name = parser.arg1()
                num_args = parser.arg2()
                self.code_writer.writeCall(function_name, num_args)