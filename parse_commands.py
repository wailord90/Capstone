import os
import re
import sys

def main(argv):
    print("yup")
    os.system("ausearch -ua root -i | grep cmd -B 3 > tmpfile.txt")
    with open('tmpfile.txt', 'r') as infile:
        lines = []
        for line in infile:
            lines.append(line)
            if len(lines) >= 3:
                parse(lines)
                lines = []
        if len(lines) > 0:
            parse(lines)
    print contents


def parse(lines):
    cmd = re.search("(?<=\scmd=)[a-z]+",lines)
    uid = re.search("(?<=\suid=)[a-z]+",lines)
    auid = re.search("(?<=\sauid=)[a-z]+",lines)
    time = re.search("([0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+:[0-9]+.[0-9]+:[0-9]+)",lines)
    proctitle = re.search("(?<=proctitle=)[a-z]+",lines)
    print auid +" "+ uid +" "+ time  +" "+ cmd +" "+ proctitle



if __name__ == '__main__':
    main(sys.argv[1:])
