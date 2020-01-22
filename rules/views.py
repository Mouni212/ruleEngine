from django.shortcuts import render
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rules import monitoring
from .models import Rule
from .utils.exceptions import exceptions

@csrf_exempt
def create_rule(request):

    if request.method == 'POST':
        print("Here in post")
        rules_input = json.loads(request.body)
        rule_name = rules_input["name"]
        rule = rules_input["rule"]
        name_space = rules_input["namespace"]
        action_url_map = []
        action_urls = rules_input["actions"]
        for action_url in action_urls:
            action_url_map.append([action_url["name"], action_url["url"]])

        freq = rules_input["frequency"]
        try:
            monitoring.create_rule(name_space, rule, rule_name, action_url_map, freq)
        except Exception as e:
            #print(e)
            return HttpResponse(str(e), status=400)

        return HttpResponse("201 return code")


def get_rule(request):
    if request.method == 'GET':
        rules = Rule.objects.all()
        rules_json = json.dumps(rules)
        return JsonResponse(rules_json)

@csrf_exempt
def delete_rule(request):
    if request.method == 'POST':
        rule_name_input = json.loads(request.body)
        rule_name = rule_name_input["rule_name"]
        print(rule_name)
        monitoring.delete_rule(rule_name)
        return HttpResponse("201 return code")




