from django.http import HttpResponse

from .models import RuleAction, Rule, Action
from .utils import operators
from .utils.exceptions import exceptions

def validate_evaluate(rule, logs):
    word_list = rule.split(" ")
    rules = ""
    list_length = len(word_list)
    i = 0
    while i < list_length:
        operator_handler = operators.operator_dictionary.get(word_list[i])
        if operator_handler is not None:
            operators_obj = (operators.str_to_class(operator_handler))
            try:
                print(word_list[i+2])
                result = operators_obj.evaluate(column_name=word_list[i + 1], begin_time_given = word_list[i + 2])
                i = i + 3
                rules += result
            except:
                raise exceptions.Invalid("Rule is not valid")
        else:
            rules += word_list[i]
            i = i+1
        rules += " "
    try:
        result_value = eval(rules)
        return result_value
    except:
        raise exceptions.Invalid("Rule is not valid")


def is_valid_url(param):
    return True


def modify_action_url_map(action_url_map, logs):
    action_url_list = []
    if len(action_url_map) == 0:
        return None
    for i in range(len(action_url_map)):
        print(action_url_map)
        action_id = Action.get_id_from_name(action_url_map[i][0], logs)

        if(action_id is not None and is_valid_url(action_url_map[i][1])):
            action_url_list.append([action_id, action_url_map[i][1]])
        else:
            if action_id is None:
                raise exceptions.Invalid("action_id_null_error")
            else:
                raise exceptions.Invalid("Value is not valid")
    return action_url_list


def rule_existence(rule_condition, name_space):
    if Rule.get_rule(rule_condition) is not None and :
        return False
    else:
        return True


def create_rule(name_space, rule_condition, rule_name, action_url_map, freq):
    logs = []
    try:
        is_valid_rule = validate_evaluate(rule_condition, logs)
    except Exception as e:
        raise e
        #return HttpResponse("404")

    if is_valid_rule is None:
        raise exceptions.Invalid("not_valid_rule_error")
        return false

    try:
        action_url_map = modify_action_url_map(action_url_map, logs)
    except exceptions.Invalid as e:
        raise

    if action_url_map is None:
        raise exceptions.Invalid("empty_action_url_map_error")
        return false
    rule_exist = rule_existence(rule_condition, name_space)
    rule_id = Rule.insert_into_rule_table(name_space, rule_condition, rule_name, freq, logs)

    for action_url in action_url_map:
        action_id = action_url[0]
        url = action_url[1]
        RuleAction.insert_into_rule_action_table(rule_id, action_id, url, logs)

    return logs


def check_condition():
    logs = []

    print("Laptop Table created successfully ")

    return


def delete_rule(rule_name):
    rule_list = Rule.objects.filter(rule_name = rule_name)
    for rule in rule_list:
        rule.is_active = False
        rule.save()
        action_rules = RuleAction.objects.filter(rule_id=rule.rule_id)
        for action_rule in action_rules:
            action_rule.is_active = False
            action_rule.save()
    return

