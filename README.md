# Dummy
is a simple RISCV Compiler for the Dummy language.
## Tokens:
PAREN = '\[()]' \
SEMICOLON = ';' \
NUMBER = '\[0-9]+' \
IDENTIFIER = '\[a-zA-Z_][a-zA-Z0-9_]*' \
OPERATOR = '\[+\-\*/]'\
SKIP = '\[ \\t\\n\\r]'
## Grammar:
prog -> stmt_list \
stmt_list -> stmt stmt_list | epsilon \
stmt -> expr_stmt | assign_stmt \
expr_stmt -> add_expr SEMICOLON \
add_expr -> mul_expr mul_tail \
mul_tail -> ADD_OP mul_expr | epsilon \
mul_expr -> factor mul_tail \
mul_tail -> MUL_OP factor | epsilon \
factor -> NUMBER | IDENTIFIER | ( expr ) \
assign_stmt -> ID EQUALS expr_stmt SEMICOLON \
\
The Grammar is parsed by a recursive descent parser.
## Usage:
To compile a file using the Dummy-Syntax simply call the **compile.py** with following arguments:
- \-i source file (neccesary)
- \-o output file (default is output.asm)
- \-q quiet (no console output while compiling)
- \-d debug (prints every evaluated statement in assembly)
## Example:
```bash
a = (5 - 2) * 3;
(a + 4) - (a + 2);
a = a + a;
b = a * a * 2;
```
Have fun!
