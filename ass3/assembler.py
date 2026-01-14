import os
import sys

from .code.code import Code
from .parsing import parser


def usage():
    print("Usage:")
    print(" python assembler.py <filename>.asm")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    code_file = sys.argv[1]
    code_text = open(code_file, 'r')

    print("Calling parser...")
    code: Code = parser.parse_text(code_text)
    code_text.close()
    print("Code parsed.\n")

    #print(code.to_string())

    print("Starting first pass...")
    symbol_table = code.first_pass()
    print("Symbol table: " + str(symbol_table))
    print(code.get_header() + "\n")

    print("Starting second pass...\n")
    code.second_pass()

    file_name = os.path.splitext(os.path.basename(code_file))[0]

    with open(file_name + ".obj", "w") as f:
        f.write(code.object_program)

    with open(file_name + ".lst", "w") as f:
        f.write(code.lst_to_string())

    print("Finished successfully.")




if __name__ == "__main__":
    main()