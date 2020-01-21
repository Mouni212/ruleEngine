from django.shortcuts import render
import json
from django.http import JsonResponse

# Create your views here.
from rules import Monitoring
from .models import Rule


def create_rule(request):

    if request.method == 'POST':
        rules_input = json.loads(request.body)
        rule_name = rules_input["name"]
        rule = rules_input["rule"]
        name_space = rules_input["namespace"]
        action_url_map = {}
        action_urls = rules_input["actions"]
        for action_url in action_urls:
            action_url_map[action_url["name"]] = action_url["url"]

        freq = rules_input["frequency"]
        Monitoring.create_rule(name_space, rule, rule_name, action_url_map, freq)


def get_rule(request):
    if request.method == 'GET':
        rules = Rule.objects.all()
        rules_json = json.dumps(rules)
        return JsonResponse(rules_json)


def delete_rule(request):
    if request.method == 'POST':
        rule_name_input = json.loads(request.body)
        rule_name = rule_name_input["rule_name"]
        Monitoring.delete_rule(rule_name)


