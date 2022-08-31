"""
The CUI
"""
import copy

from sql import DBObj
from math import ceil

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
        query_refine(db, pre_setting_value)

    except Exception as e:
        # print("Error caught: %s" % e)
        # CHANGE ME !!!
        raise e
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

        target = ask_user_target()
    except Exception as e:
        raise Exception(e)

    return {"schema": schema, "table": table, "target": target, "attributes": attributes}


def query_refine(db, pre_setting_value):
    attribute_settings = []
    for attribute in pre_setting_value["attributes"]:
        attribute_settings.append({"name": attribute,
                                   "range": db.get_attribute_possible_range([], attribute), "user_set": False})
    while True:
        tuple_est = get_estimate(db, attribute_settings)

        print("=========================================")
        print(f"Current range ({tuple_est} est. tuples within this range)")
        target = pre_setting_value["target"]
        print(f"Your target: {target}")
        attribute_range_update(db, attribute_settings)
        attribute_range_printing(attribute_settings)
        make_suggestion(db, pre_setting_value["target"], tuple_est, attribute_settings)
        print("=========================================")
        print("Please select the attribute you want to change")
        user_choice_of_attribute = ask_user_choice(pre_setting_value["attributes"])
        new_range = ask_user_new_range(attribute_settings[user_choice_of_attribute]['range'])
        new_range = (int(new_range[0]), int(new_range[1]))
        attribute_settings[user_choice_of_attribute]['range'] = new_range
        attribute_settings[user_choice_of_attribute]['user_set'] = True


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
    if (choices is None) or (type(choices) == int) or (len(choices) == 0):
        return False
    for choice in choices:
        if (choice >= choices_len) or (choice < 0):
            return False
    return True


def ask_user_new_range(range):
    range_input_is_valid = False
    while not range_input_is_valid:
        user_input = input("Please input the new range, format: min, max\n")
        if (len(user_input.split(',')) != 2):
            print("Invalid input, please try again")
            continue

        min = user_input.split(',')[0].strip()
        max = user_input.split(',')[1].strip()

        if (not min.isnumeric()) or (not max.isnumeric()):
            print("Invalid input, please try again")
        elif (int(min) > range[1]):
            print("Invalid input, max value should be smaller or equal to the original max value")
        elif (int(max) < range[0]):
            print("Invalid input, min value should be larger or equal to the original min value")
        else:
            range_input_is_valid = True

    return (min,max)

def attribute_range_update(db, attribute_settings):
    user_edited_attributes = {}
    for attribute in attribute_settings:
        if attribute['user_set']:
            user_edited_attributes[attribute['name']] = attribute['range']
    for attribute in attribute_settings:
        if not attribute['user_set']:
            attribute['range'] = db.get_attribute_possible_range(user_edited_attributes, attribute['name'])

def attribute_range_printing(attribute_setting):
    for attr in attribute_setting:
        if (attr['user_set']):
            print(f"{attr['name']}*: {attr['range']}")
        else:
            print(f"{attr['name']}: {attr['range']}")

    return


def ask_user_target():
    target = "-"
    while not target.isnumeric():
        target = input("Please input the target value: ")
    return int(target)


def make_suggestion(db, target, est, attribute_settings):
    if target < est:
        min_variations = est
        curr_suggestion = {"name": "", "range": (0, 0)}
        for attr_no in range(len(attribute_settings)):
            #if not attribute_settings[attr_no]['user_set']:
                temp_attribute_settings = copy.deepcopy(attribute_settings)
                attr = temp_attribute_settings[attr_no]
                original_low = attr['range'][0]
                low = attr['range'][0]
                high = attr['range'][1]
                mid = (low + high) // 2
                attr["user_set"] = True
                while low < high - 1:
                    mid = int((low + high) // 2)
                    attr['range'] = (original_low, mid)
                    curr_est = get_estimate(db, temp_attribute_settings)
                    if curr_est < target:
                        low = mid
                    else:
                        high = mid
                curr_est = get_estimate(db, temp_attribute_settings)
                # print(f"Current attribute: {attr['name']}, curr est: {mid} @ {curr_est}. " )
                if abs(get_estimate(db, temp_attribute_settings) - target) < min_variations:
                    min_variations = abs(get_estimate(db, temp_attribute_settings) - target)
                    curr_suggestion = [attr["name"],(attribute_settings[attr_no]["range"][0], mid)]
        print("Suggestion: Set %s to %s" % (curr_suggestion[0], curr_suggestion[1]))
    else:
        print("Your target is equal to the current estimate of result.")


def get_estimate(db, attribute_settings):
    user_edited_attributes = {}
    for attribute in attribute_settings:
        if (attribute["user_set"]):
            user_edited_attributes[attribute["name"]] = attribute["range"]
    return db.get_current_estimate(user_edited_attributes)
