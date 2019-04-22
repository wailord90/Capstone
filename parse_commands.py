import os
import re
import sys

def main(argv):
    print("yup")
    os.system("ausearch -ua root -i | grep cmd -B 3 > tmpfile.txt")
    file = open("tmpfile.txt", "r")
    contents = f.read()
    print contents


def parse():
    re.search


if __name__ == '__main__':
    main(sys.argv[1:])
