# === ILOC Instructions ===
# load r1 => r2 === r2 MEM[r1]
# loadI c => r2 === r2 = c
# store r1 => r2 === MEM[r2] =r1
# add r1, r2 => r3 === r3 = r1 + r2
# sub r1, r2 => r3 === r3 = r1 - r2
# mult r1, r2 => r3 === r3 = r1 * r2
# lshift r1, r2 => r3 === r3 = r1 << r2
# rshift r1, r2 => r3 === r3 = r1 >> r2
# output r1 === Print MEM[r1]
# nop === No operation


# === Operand Rules ===
# Register: r followed by a non-negative integer (e.g., r0, r1, r25, r003)
# Constant: non-negative integer (0 - 2^31-1)
# Assignment Arrow: => (no space inside)
# Commas separate operands for 2-operand instructions
# Comments start with // and extedn to the end of the line
# One instruction per line
class TokenType:
    OPCODE = "OPCODE"
    REGISTER = "REGISTER"
    CONSTANT = "CONSTANT"
    COMMA = "COMMA"
    ASSIGN_ARROW = "=>"
    ENDLINE = "ENDLINE"
    COMMENT = "//"
    WHITESPACE = "WHITESPACE"


ILOC_INSTRUCTIONS = {
    "load", "loadI", "store", "add", "sub", "mult", "lshift", "rshift", "output", "nop"
}

def char_by_char_scanner(self):
    while self.pos < self.length:
        char = self.peek()