import sys
import os


def main(argv):
    if argv[1].startswith('CtLiteral') and argv[0] in argv[1]:
        print(argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])
