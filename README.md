Group 17

1. KWASHIE KLENAM CHRISTIAN - 1724421118
2. SABINAR ARTHUR - 1725885883
3. NII ANTIEYE TETTEH AARON - 2425430128
4. SAMUEL ADU-BOAHEN - 1722697089
5. EDWARD AGYEI OKYERE - 2425430115
6. NTI KOFI TWUMASI - 1725303859
7. OKORLEY EMMANUEL TETTEY - 1723727635
8. OSEI PHILLIP - 2425430016
9. PRINCE OFORI - 1727338141
10. PRINCE TETTEH - 1725385412

## How to Run 
For Linux Distributions, the progam is wrapped in a shell script named `411fe`. 
To ensure it has execution permissions, run:
```shell
chmod +x 411fe
```
To run the program in `411fe.py` file:
For Mac/Linux users:
```shell
python3 411fe.py -[flags] <filename>
```

For Windows:
```shell
python 411fe.py -[flags] <filename>
```

### Command Line Flags
The progam supports the following modes:

* `-h` : This displays the help message and list of valid arguments.
* `-s` <filename> : This scans the list of input file and prints the list of tokens (<Line> <TokenType> <Lexeme>)
* `-p` <filename> : This scans and parses the file. If valid, it prints "VALID ILOC PROGRAM", or lists syntax error with line numbers (Default behavior).
* `-r` <filename> : This scans, parses and contructs the Intermediate Representation. It prints the IR in human-readable format.

## Implementation
* **Scanner**: Implemented as a character-by-character scanner to help recognize all specified tokens.
* **Parser**: Validates opcode signatures and operand formats line-by-line.
* **IR**: Constructs a list of instruction objects containing opcode, line number, and parsed operands.

### Supported ILOC Subset
* **Opcodes**: `load`, `loadI`, `store`, `add`, `sub`, mult`, `lshift`, `rshift`, `output`, `nop` 
* **Comments**: Lines starting with `//`
* **Operands**: Registers (`r` + non-negative int), Constants (non-negative int).
