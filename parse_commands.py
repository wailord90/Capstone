import os
import re
import sys
from db_orch import add_session


def main(argv):

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
    cmd = re.search(r'(?<=\scmd=)[a-z]+', lines)
    if cmd:
        cmd = cmd.group(0)
    else:
        cmd = "none"
    uid = re.search("(?<=\suid=)[a-z]+", lines)
    if uid:
        uid = uid.group(0)
    else:
        uid = "none"
    auid = re.search("(?<=\sauid=)[a-z]+", lines)
    if auid:
        auid = auid.group(0)
    else:
        auid = "none"
    time = re.search(
        "([0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+:[0-9]+.[0-9]+)", lines)
    if time:
        time = time.group(0)
    else:
        time = "none"
    proctitle = re.search("(?<=proctitle=)[a-z]+", lines)
    if proctitle:
        proctitle = proctitle.group(0)
    else:
        proctitle = "none"
    type = re.search('a0=sh', lines)
    a2 = re.search('(?<=\sa2=)(.+?),', lines)
    if type:
        if a2:
            a2 = a2.group(0)
        else:
            a2 = "none"
    else:
        a2 = "none"
    pid = re.search('(?<=pid=)[0-9]+', lines)
    if pid:
        pid = pid.group(0)
    else:
        pid = "none"
    cwd = re.search('(?<=cwd=).+?\s', lines)
    if cwd:
        cwd = cwd.group(0)
    else:
        cwd = "none"
    print lines
    
    if cmd != "none" or a2 != "none":
        add_session(time, uid, auid, cwd, pid, a2, cmd,host = os.popen("hostname").read(), flag="none")



if __name__ == '__main__':
    main(sys.argv[1:])
