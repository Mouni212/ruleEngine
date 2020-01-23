from . import operator_handlers
from .models import RuleAction, Rule, Action
from common.exceptions import exceptions


def validate_evaluate(rule_condition):
    word_list = rule_condition.split(" ")
    rules = ""
    list_length = len(word_list)
    i = 0
    while i < list_length:
        try:
            operator_handler = operator_handlers.operator_dictionary.get(word_list[i])
        except Exception as e:
            raise e
        if operator_handler is not None:
            try:
                result = operator_handler(name=word_list[i]).evaluate(metric_name=word_list[i + 1], begin_time_given=word_list[i + 2])
                i = i + 3
                rules += result
            except Exception as e:
                raise exceptions.InvalidException("Rule is not valid")
        else:
            rules += word_list[i]
            i = i+1
        rules += " "
    try:
        print("RULES " + str(rules))
        result_value = eval(rules)
        if result_value is True:
            [True, ]
        return result_value,
    except:
        raise exceptions.InvalidException("Rule is not valid")


def is_valid_value(param):
    return True


def modify_action_value_map(action_value_map):
    action_value_list = []
    if len(action_value_map) == 0:
        return None
    for i in range(len(action_value_map)):
        print(action_value_map)
        action_id = Action.get_id_from_name(action_value_map[i][0])

        if(action_id is not None and is_valid_value(action_value_map[i][1])):
            action_value_list.append([action_id, action_value_map[i][1]])
        else:
            if action_id is None:
                raise exceptions.InvalidException("action_id_null_error")
            else:
                raise exceptions.InvalidException("Value is not valid")
    return action_value_list


def create_rule(name_space, rule_condition, rule_name, action_value_map, freq):
    try:
        is_valid_rule = validate_evaluate(rule_condition)
    except Exception as e:
        raise e

    if is_valid_rule is None:
        raise exceptions.InvalidException("not_valid_rule_error")
        return false

    try:
        action_value_map = modify_action_value_map(action_value_map)
    except Exception as e:
        raise e

    if action_value_map is None:
        raise exceptions.InvalidException("empty_action_value_map_error")
        return false
    rule_id = Rule.rule_existence(rule_name, name_space)
    if rule_id is not None:
        Rule.update(rule_id, rule_condition, freq)
    else:
        try:
            rule_id = Rule.insert_into_rule_table(name_space, rule_condition, rule_name, freq)
        except Exception as e:
            raise e

    for action_value in action_value_map:
        action_id = action_value[0]
        value = action_value[1]
        try:
            RuleAction.insert_into_rule_action_table(rule_id, action_id, value)
        except Exception as e:
            raise e


def delete_rule(rule_name):
    rule_list = Rule.objects.filter(name=rule_name)
    if len(rule_list) == 0:
        raise exceptions.InvalidException(rule_name + " doesn't exist")
    else:
        for rule in rule_list:
            rule.is_active = False
            rule.save()
            action_rules = RuleAction.objects.filter(id=rule.id)
            for action_rule in action_rules:
                action_rule.is_active = False
                action_rule.save()
    return

