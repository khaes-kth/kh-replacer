import sys
import os


def main(argv):
    line = input()
    while (line):
        if line.startswith('CtLiteral') and argv[0] in line:
            print(line)
        try:
            line = input()
        except:
            break

if __name__ == "__main__":
    main(sys.argv[1:])
