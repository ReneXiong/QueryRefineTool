"""
The CUI
"""

from sql import DBObj
import sql_list


def ui(argv):
    argv_check_result = check_length_argv(argv)
    pre_setting_value = {}
    if argv_check_result != 0:
        raise Exception("Error: Invalid Argument")

    db = DBObj(argv[1], argv[2], argv[3], argv[4], argv[5])
    try:
        db.connect()
        pre_setting_value = pre_setting(db)
        print("pre-setting-finished")
        while True:
            query_refine(db)

    except Exception as e:
        print("Error caught: %s" % e)
    finally:
        db.close()

    return 0


def pre_setting(db):
    try:
        print("Your database contains these schemas"
              "please input the index you want to select")
        all_schema_names = db.get_all_schema_names()
        schema = all_schema_names[ask_user_choice(all_schema_names)]

        print(f"The schema you have chosen is {schema}.\n"
              "It contains these tables, please input the index you want to select")
        all_table_names = db.get_all_table_names(schema)
        table = all_table_names[ask_user_choice(all_table_names)]

        print(f"The table you have chosen is {schema}.\"{table}\".\n"
              "It contains these int attributes, please input the index you want to select")
        print("You need select at least two, divided by comma. Example:")
        print("1,3,5,6")
        all_attributes_names = db.get_all_int_attributes(table)
        user_input_attributes = ask_user_attributes(all_attributes_names)
        attributes = []
        attributes_selected_string = ""
        for i in user_input_attributes:
            attributes += [all_attributes_names[i]]
            attributes_selected_string.join(f"{i}.{all_attributes_names[i]} ")
        print("Attributes you have chosen is " + ", ".join(attributes))
    except Exception as e:
        raise Exception(e)

    return {"schema": schema, "table": table, "attributes": attributes}


def query_refine(db):
    tuple_est = db.get_current_estimate()
    print(f"Current range ({tuple_est} est. tuples within this range)")
    print("    ".join(db.get_attribute_range())) # TODO
    print("Please select the attribute you want to change")
    ask_user_choice(db.get_attribute())
    ask_user_new_range()


def check_length_argv(argv):
    if argv is None:
        print("Error: No Argument")
        return -1
    if len(argv) != 6:
        return -2
    else:
        print("user args: %s" % argv)
        return 0


def ask_user_choice(all_choices):
    string_ask_for_input = ""
    count = 0

    for name in all_choices:
        string_ask_for_input += "%d. %s, " % (count, name)
        count += 1

    choice = input(string_ask_for_input + '\n')
    while (not choice.isdigit()) or \
            (int(choice) < 0) or \
            (int(choice) > len(all_choices)):
        choice = input("Invalid input, please try again: ")

    return int(choice)


def ask_user_attributes(all_choices):
    string_ask_for_input = ""
    count = 0

    for name in all_choices:
        string_ask_for_input += "%d. %s, " % (count, name)
        count += 1

    choices = eval(input('\n' + string_ask_for_input + '\n'))
    while not user_attributes_input_is_validate(choices, len(all_choices)):
        print("\n Invalid input, please try again:")
        choices = eval(input('\n' + string_ask_for_input + '\n'))

    return choices


def user_attributes_input_is_validate(choices, choices_len):
    if (choices is None) or (len(choices) == 0):
        return False
    for choice in choices:
        if (choice >= choices_len) or (choice < 0):
            return False
    return True


def ask_user_new_range():
    # TODO
    pass
