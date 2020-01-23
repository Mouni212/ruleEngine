from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rules import monitoring
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

        freq = rules_input["frequency"]
        try:
            monitoring.create_rule(name_space, rule_condition, rule_name, action_value_map, freq)
        except Exception as e:
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
            monitoring.delete_rule(rule_name)
        except Exception as e:
            return HttpResponse(str(e))
        return HttpResponse("201 return code")




