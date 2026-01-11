
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
    print("Code parsed.")
    #print(code.to_string())




if __name__ == "__main__":
    main()