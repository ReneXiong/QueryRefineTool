"""
The CUI
"""

from sql import sqlObj

def testhaha(a, b):
    print(a + b)


def ui(argv):
    if argv is None:
        print("Error: No Argument")
        return -1
    if len(argv) != 5:
        return -2
    else:
        print("user args: %s" % argv)

    print(testhaha(1, 1))
