import sys
import Mparser
import scanner
from TreePrinter import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)

    if not Mparser.error_occurred:
        ast.printTree()
    else:
        print("Parsing failed!")
