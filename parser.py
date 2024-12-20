class Parser:
    """Read and parses an instruction"""

    def __init__(self, path):
        self.path = path
        self.file = open(self.path)
        self.lines = self.file.readlines()
        self.index = -1  # Line index of the file (including empty spaces)
        self.line_index = 0  # Line index of the instructions (not including empty spaces)
        self.line = None
        self.arithmetics = ["add", "sub", "neg", "eq", "and", "or", "not", "gt", "lt"]
        self.C_ARITHMETIC = "C_ARITHMETIC"
        self.C_PUSH = "C_PUSH"
        self.C_POP = "C_POP"
        self.C_LABEL = "C_LABEL"
        self.C_GOTO = "C_GOTO"
        self.C_IF = "C_IF"
        self.C_FUNCTION = "C_FUNCTION"
        self.C_RETURN = "C_RETURN"
        self.C_CALL = "C_CALL"

    def __str__(self):
        return self.line

    def __len__(self):
        return len(self.line)

    def hasMoreLines(self):
        """Returns true if there are more commands in the file."""
        return self.index + 1 < len(self.lines)

    def advance(self):
        """Reads the next instruction from the file and makes it the current instruction."""
        self.line = self.get_next_line()
        while self.line and len(self.line) == 0:  # Skip empty lines
            if not self.hasMoreLines():
                return None
            self.line = self.get_next_line()

        return self.line

    def get_next_line(self):
        """Gets the next line, removing comments and whitespace."""
        self.index += 1
        if self.index >= len(self.lines):
            return None
        dirty_line = self.lines[self.index]
        return dirty_line.split("//")[0].strip()  # Remove whitespace and comments

    def command_type(self):
        """Returns the type of the current command."""
        if not self.line:
            return None

        # Get first word of command
        command = self.line.split(" ")[0]

        # Check arithmetic commands
        if command in self.arithmetics:
            return self.C_ARITHMETIC

        # Map commands to their types
        command_types = {
            'push': self.C_PUSH,
            'pop': self.C_POP,
            'label': self.C_LABEL,
            'goto': self.C_GOTO,
            'if-goto': self.C_IF,
            'function': self.C_FUNCTION,
            'return': self.C_RETURN,
            'call': self.C_CALL
        }

        return command_types.get(command)


    def arg1(self):
        if self.command_type() == self.C_RETURN:
            return None
        if self.command_type() == self.C_ARITHMETIC:
            return self.line.split(" ")[0]
        else:
            return self.line.split(" ")[1]

    def arg2(self):
        if self.command_type() in [self.C_PUSH, self.C_POP, self.C_FUNCTION, self.C_CALL]:
            return int(self.line.split(" ")[2])
        return None
