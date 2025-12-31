import sys

# CONSTANTS
OPCODES = {
    'load', 'loadI', 'store', 'add', 'sub', 
    'mult', 'lshift', 'rshift', 'output', 'nop'
}

# PART A: SCANNER 
class Scanner:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.tokens = []
    
    def scan(self):
        # Character-by-character scanning loop
        while self.position < len(self.source):
            char = self.source[self.position]

            if char in ' \t\r': # Whitespace (ignored)
                self.position += 1
            elif char == '\n':
                self.line += 1
                self.position += 1
            elif char == '/' and self.match('/'): # Comments
                lexeme = '//'
                while self.position < len(self.source) and self.source[self.position] != '\n':
                    lexeme += self.advance()
                self.tokens.append((self.line, 'COMMENT', lexeme))
            elif char == '=' and self.match('>'): # Assign Arrow 
                self.tokens.append((self.line, 'ASSIGN_ARROW', '=>'))
            elif char == ',': # Comma
                self.tokens.append((self.line, 'COMMA', ','))
                self.position += 1
            elif char.isdigit(): # Constants
                lexeme = self.advance()
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    lexeme += self.advance()
                self.tokens.append((self.line, 'CONSTANT', lexeme))
            elif char.isalpha(): # Words (Opcode or Register)
                lexeme = self.advance()
                while self.position < len(self.source) and self.source[self.position].isalnum():
                    lexeme += self.advance()
                
                if lexeme in OPCODES:
                    self.tokens.append((self.line, 'OPCODE', lexeme))
                elif lexeme.startswith('r') and lexeme[1:].isdigit():
                    self.tokens.append((self.line, 'REGISTER', lexeme)) 
                else:
                    # Per instructions, report scan errors
                    print(f"Error on line {self.line}: Invalid identifier '{lexeme}'")
            else:
                # Handle unexpected characters
                print(f"Error on line {self.line}: Unexpected character '{char}'")
                self.position += 1
        return self.tokens

    def advance(self):
        if self.position >= len(self.source):
            return ''
        char = self.source[self.position]
        self.position += 1
        return char
    
    def match(self, expected):
        if self.position + 1 < len(self.source) and self.source[self.position + 1] == expected:
            self.position += 2
            return True
        return False

# PART B: PARSER 
class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t[1] != 'COMMENT']
        self.pos = 0
        self.ir = []
        self.errors = []

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type, error_msg):
        curr = self.current()
        if curr and curr[1] == expected_type:
            self.pos += 1
            return curr[2]
        else:
            line = curr[0] if curr else 'EOF'
            self.errors.append(f"Error on line {line}: {error_msg}")
            return None

    def parse(self):
        while self.pos < len(self.tokens):
            curr = self.current()
            
            if curr[1] != 'OPCODE':
                self.errors.append(f"Error on line {curr[0]}: Expected Opcode, got {curr[1]}")
                self.pos += 1
                continue
            
            opcode = curr[2]
            line = curr[0]
            self.pos += 1 

            try:
                if opcode in ['add', 'sub', 'mult', 'lshift', 'rshift']:
                    r1 = self.consume('REGISTER', "Missing first operand")
                    self.consume('COMMA', "Missing comma between operands")
                    r2 = self.consume('REGISTER', "Missing second operand")
                    self.consume('ASSIGN_ARROW', "Invalid assignment arrow")
                    r3 = self.consume('REGISTER', "Missing destination register")
                    if r1 and r2 and r3:
                        self.ir.append(IRNode(line, opcode, r1, r2, r3))

                # 2. Memory operations: load r1 => r2 (or store r1 => r2)
                elif opcode in ['load', 'store']:
                    r1 = self.consume('REGISTER', "Missing source operand")
                    self.consume('ASSIGN_ARROW', "Invalid assignment arrow")
                    r2 = self.consume('REGISTER', "Missing destination register")
                    if r1 and r2:
                        self.ir.append(IRNode(line, opcode, r1, r2))

                # 3. Immediate load: loadI c => r2
                elif opcode == 'loadI':
                    val = self.consume('CONSTANT', "Missing constant value")
                    self.consume('ASSIGN_ARROW', "Invalid assignment arrow")
                    r2 = self.consume('REGISTER', "Missing destination register")
                    if val and r2:
                        self.ir.append(IRNode(line, opcode, val, r2))

                # 4. Output: output r1
                elif opcode == 'output':
                    r1 = self.consume('REGISTER', "Missing operand after 'output'")
                    if r1:
                        self.ir.append(IRNode(line, opcode, r1))

                # 5. Nop 
                elif opcode == 'nop':
                    self.ir.append(IRNode(line, opcode))
                
            except Exception:
                self.pos += 1

# PART C: INTERMEDIATE REPRESENTATION 
class IRNode:
    def __init__(self, line, opcode, op1=None, op2=None, op3=None):
        self.line = line
        self.opcode = opcode
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        out = f"Line {self.line}: {self.opcode}"
        if self.opcode in ['add', 'sub', 'mult', 'lshift', 'rshift']:
            out += f"\n  src1: {self.op1}\n  src2: {self.op2}\n  dest: {self.op3}"
        elif self.opcode in ['load', 'store']:
            out += f"\n  src: {self.op1}\n  dest: {self.op2}"
        elif self.opcode == 'loadI':
            out += f"\n  val: {self.op1}\n  dest: {self.op2}"
        elif self.opcode == 'output':
            out += f"\n  src: {self.op1}"
        return out


# PART D: COMMAND LINE INTERFACE
def print_help():
    print("Usage: 411fe [flags] <filename>")
    print(" -h : Show this help message")
    print(" -s : Scan and print tokens")
    print(" -p : Scan, Parse, and report errors (Default)")
    print(" -r : Scan, Parse, and print IR")

def main():
    args = sys.argv[1:]
    
    # Priority: -h > -r > -p > -s
    if '-h' in args:
        print_help()
        return

    mode = '-p'
    if '-r' in args: mode = '-r'
    elif '-p' in args: mode = '-p'
    elif '-s' in args: mode = '-s'

    filename = '411fe'
    for arg in args:
        if arg[0] != '-':
            filename = arg
            break
    
    if not filename:
        # If no file provided, prompt usage
        print("Error: No input file specified.")
        print_help()
        return

    try:
        with open(filename, 'r') as f:
            source = f.read()
    except IOError:
        print(f"Error: Could not read file {filename}")
        return

    # 1. Scan
    scanner = Scanner(source)
    tokens = scanner.scan()

    # Handle -s Flag
    if mode == '-s':
        for token in tokens:
            # Output format: <lineNumber> <tokenType> <lexeme>
            print(f"{token[0]} {token[1]} {token[2]}")
        return

    # 2. Parse
    parser = Parser(tokens)
    parser.parse()

    # Handle -p Flag
    if parser.errors:
        for error in parser.errors:
            print(error)
    else:
        if mode == '-p':
            print("VALID ILOC PROGRAM")
        
        # Handle -r Flag
        elif mode == '-r':
            for node in parser.ir:
                print(node)

if __name__ == "__main__":
    main()
