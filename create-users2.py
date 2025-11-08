#!/usr/bin/python3

import os
import re
import sys

# enable dry-run mode if argument --dry-run is provided
DRYRUN = False
if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
    DRYRUN = True

def main():
    for line in sys.stdin:

        # skip comment lines
        match = re.match("^#", line)

        # split fields from input file
        fields = line.strip().split(':')

        # skip invalid lines or commented lines
        if match or len(fields) != 5:
            continue

        # extract fields
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # group list
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        if DRYRUN:
            print(cmd)
        else:
            os.system(cmd)

        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        if DRYRUN:
            print(cmd)
        else:
            os.system(cmd)

        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                if DRYRUN:
                    print(cmd)
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()
