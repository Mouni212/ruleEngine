from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from common import date_time
from rule_engine import celery
from rules import utils
from .models import Rule


@csrf_exempt
def create_rule(request):

    if request.method == 'POST':
        print("Here in post")
        rules_input = json.loads(request.body)
        rule_name = rules_input["name"]
        rule_condition = rules_input["rule_condition"]
        name_space = rules_input["namespace"]
        action_value_map = []
        action_values = rules_input["actions"]
        for action_value in action_values:
            action_value_map.append([action_value["name"], action_value["value"]])

        print("action_value_map", action_value_map)

        freq = rules_input["frequency"]
        try:
            frequency_seconds = date_time.total_seconds(freq)
        except Exception as e:
            return HttpResponse(str(e), status=400)
        #SlackHandler.apply_action()

        try:

            utils.create_rule(name_space, rule_condition, rule_name, action_value_map, frequency_seconds)
        except Exception as e:
            print(e)
            return HttpResponse(str(e), status=400)

        return HttpResponse("201 return code")


@csrf_exempt
def get_rule(request):
    if request.method == 'GET':
        rules = list(Rule.objects.all())
        return render(request, 'show_rules.html', {'rules': rules})


@csrf_exempt
def delete_rule(request):
    if request.method == 'POST':
        rule_name_input = json.loads(request.body)
        rule_name = rule_name_input["rule_name"]
        try:
            utils.delete_rule(rule_name)
        except Exception as e:
            return HttpResponse(str(e))
        return HttpResponse("201 return code")




