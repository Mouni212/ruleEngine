from .models import RuleAction, Rule, Action
from .utils import exceptions, operators


def validate_evaluate(rule):
    word_list = rule.split(" ")
    rules = ""
    list_length = word_list.size()
    for i in list_length:
        operator_handler = operators.operator_dictionary[word_list[i]]
        if operator_handler is not None:
            result = getattr(operator_handler, 'evaluate')(word_list[i+1])
            if result is not None:
                rules.append(result)
            else:
                print(" Rule Syntax is not correct")
                return None
        else:
            rules.append(word_list[i])
    return eval(rules)


def is_valid_url(param):
    return True


def modify_action_url_map(action_url_map, logs):
    action_url_list = []
    if len(action_url_map) == 0:
        return None
    for i in range(len(action_url_map)):
        action_id = Action.objects.get_id_from_name(action_url_map[0], logs)
        if action_id is not None and is_valid_url(action_url_map[1]):
            action_url_list.append([action_id, action_url_map[1]])
        else:
            if action_id is None:
                raise exceptions.action_id_null_error(logs)
            else:
                raise exceptions.invalid_url_error(logs)
    return action_url_list


def create_rule(name_space, rule_condition, rule_name, action_url_map, freq):
    logs = []

    is_valid_rule = validate_evaluate(rule_condition, logs)

    if is_valid_rule is None:
        raise exceptions.not_valid_rule_error(logs)
        return false

    action_url_map = modify_action_url_map(action_url_map, logs)

    if action_url_map is None:
        raise exceptions.empty_action_url_map_error(logs)
        return false
    rule_id = Rule.objects.insert_into_rule_table(name_space, rule_condition, rule_name, freq, logs)

    for action_url in action_url_map:
        action_id = action_url[0]
        url = action_url[1]
        RuleAction.objects.insert_into_rule_action_table(rule_id, action_id, url, logs)

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

