"""
The CUI
"""

from sql import DBObj


def ui(argv):
    argv_check_result = check_length_argv(argv)
    if(argv_check_result != 0):
        return argv_check_result

    db = DBObj(argv[1], argv[2], argv[3], argv[4], argv[5])
    try:
        db.connect()
        print("connect success")
        test_result = db.get_all_table_names()
    except Exception as e:
        print("Error_Caught: %s" % e)
    finally:
        db.close()
        print("close connection")

    return 0

def check_length_argv(argv):
    if argv is None:
        print("Error: No Argument")
        return -1
    if len(argv) != 6:
        return -2
    else:
        print("user args: %s" % argv)
        return 0