import argparse

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from codegenerator import Codegenerator

def main():
    # CLI
    parser = argparse.ArgumentParser(description="Compiler for the Dummy-language")

    parser.add_argument("-i", "--input", type=str, help="Input file to compile")
    parser.add_argument("-o", "--output", type=str, help="Output file to write to")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    parser.add_argument("-d", "--debug", action="store_true", help="Output while executing asm")

    args = parser.parse_args()

    if args.input:
        input_file = args.input
    else:
        raise Exception("[COMPILER]: Error, no input file provided!")
    if args.output:
        output_file = args.output
    else:
        print("[COMPILER]: No output file provided, using ./output.asm output file")
        output_file = "./output.asm"
    quiet_mode = args.quiet
    asm_output = args.debug
    #

    if not quiet_mode:
        print("[COMPILER]: Dummy Compiler - 2024\n")

    with open(input_file, 'r') as file:
        source_string = file.read()

    tokens = Lexer(source_string, options={"quiet": quiet_mode}).lex()

    ast = Parser(tokens, options={"quiet": quiet_mode}).parse()

    Interpreter(ast, options={"quiet": quiet_mode}).interpret()

    code = Codegenerator(ast, options={"output": asm_output, "quiet": quiet_mode}).generate()

    with open(output_file, 'w') as file:
        for line in code:
            file.write(f"{line}\n")


if __name__ == "__main__":
    main()