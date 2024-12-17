from parser import Parser
from code_writer import CodeWriter
import os
import sys


class VMTranslator:

    def __init__(self, input_path):
        self.input_path = input_path.rstrip('/')
        self.code_writer = None
        self.input_files = []

    def process_directory(self, dir_path):
        # Get directory name for output file name
        dir_name = os.path.basename(dir_path)

        # Find all .vm files in the directory
        self.input_files = [
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if f.endswith('.vm') and os.path.isfile(os.path.join(dir_path, f))
        ]

        if not self.input_files:
            raise ValueError(f"No .vm files found in {dir_path}")

        # Create output file with directory name
        output_file = os.path.join(dir_path, f"{dir_name}.asm")
        self.code_writer = CodeWriter(output_file)

        # If only one VM file, just translate it without bootstrap
        if len(self.input_files) == 1:
            self.translate_file(self.input_files[0])
            return

        # For multiple files, check if Sys.vm exists
        sys_vm_exists = any(f.endswith('Sys.vm') for f in self.input_files)

        # If multiple files and Sys.vm exists, write bootstrap ONCE at the start
        if sys_vm_exists:
            self.write_bootstrap()

        # Translate all files (Sys.vm first if it exists)
        if sys_vm_exists:
            # Find and translate Sys.vm first
            sys_file = next(f for f in self.input_files if f.endswith('Sys.vm'))
            self.translate_file(sys_file)
            remaining_files = [f for f in self.input_files if f != sys_file]
        else:
            remaining_files = self.input_files

        # Translate remaining files
        for vm_file in sorted(remaining_files):
            self.translate_file(vm_file)

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
        if os.path.isdir(self.input_path):
            self.process_directory(self.input_path)
        else:
            # Single file case
            self.input_files = [self.input_path]
            self.code_writer = CodeWriter(self.input_path.replace('.vm', '.asm'))
            self.translate_file(self.input_path)
        if self.code_writer:
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