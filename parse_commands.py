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


def parse(lines):
    lines = str(lines)
    print lines
    cmd = re.search(r'(?<=\scmd=)[a-z]+',lines)
    if cmd:
        cmd = cmd.group(0)
    else:
        cmd ="none"
    uid = re.search("(?<=\suid=)[a-z]+",lines)
    if uid:
        uid= uid.group(0)
    else:
        uid="none"
    auid = re.search("(?<=\sauid=)[a-z]+",lines)
    if auid:
        auid= auid.group(0)
    else:
        auid= "none"
    time = re.search("([0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+:[0-9]+.[0-9]+:[0-9]+)",lines)
    if time:
        print time
        time=time.group(0)
    else:
        time ="none"
    proctitle = re.search("(?<=proctitle=)[a-z]+",lines)
    if proctitle:
        proctitle = proctitle.group(0)
    else:
        proctitle = "none"
    print auid +" "
    print uid +" "
    print time  +" "
    print cmd +" "
    print proctitle

if __name__ == '__main__':
    main(sys.argv[1:])
