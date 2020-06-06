

from __future__ import absolute_import
import datetime
import os
import random
from celery import Celery
import sys
import csv

from django.conf import settings
from celery.schedules import crontab


## variable_list for metric_ data
namespace_list = ["Recommendation", "Bookmarking"]
metric_index_list = ["Response_time"]

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rule_engine.settings')
app = Celery('rule_engine')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
CELERY_TIMEZONE = 'UTC'

app.autodiscover_tasks()


@app.task(name="rule_evaluator", queue='celery')
def evaluate(rule_id):
    from rule_action import action_handler
    from rule_action.action_handler import action_dictionary
    from rules import utils
    from rules.models import RuleAction, Rule

    rule = Rule.objects.get(id=rule_id, is_active=True)
    result = utils.validate_evaluate(rule.rule_condition)
    if result is True:
        rule_actions = list(RuleAction.objects.filter(id=rule_id).values_list('action__name', 'value'))
        for rule_action in rule_actions:
            handler = action_dictionary.get(rule_action[0])
            if handler is not None:
                #handler.apply_action(rule_action[1], msg=rule.name+" state is now ALARM")
                handler.apply_action('https://hooks.slack.com/services/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',msg=rule.name + " state is now ALARM")
    return


@app.task(queue='celery')
def fetch_all_rules():
    from rule_action import action_handler
    from rule_action.action_handler import action_dictionary
    from rules import utils
    from rules.models import RuleAction, Rule

    active_rule_list = list(Rule.objects.filter(is_active=True).values_list('id', flat=True))
    print((active_rule_list))
    for rule_id in active_rule_list:
        evaluate(rule_id)


namespace_list = ["Recommendation", "Bookmarking"]
metric_index_list = ["Response_time"]
initial_date = [datetime.datetime(2015, 5, 27, 12, 4, 5)]
current_date = [datetime.datetime(2015, 5, 27, 12, 4, 5)]

@app.task(queue='celery')
def generate_metric_data():
    from rules.models import MetricData
    from rule_action.action_handler import SlackHandler
    #for i in range(100):
    current_date[0] = current_date[0] + datetime.timedelta(days=1)
    metric_low_range = 0
    metric_high_range = 50
    days = (current_date[0] - initial_date[0]).days
    if (39 < days < 42) or (147 < days < 150):
        metric_low_range = 200
        metric_high_range = 250
    namespace = random.choice(namespace_list)
    index = random.choice(metric_index_list)
    metric_value = random.randrange(metric_low_range, metric_high_range, 10)
    MetricData.create_entry(namespace, index, metric_value,  current_date[0])
    mycsvrow = [ current_date[0], metric_value]
    with open('document.csv', 'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(mycsvrow)
        #mysql_to_csv()

def mysql_to_csv():
    from rules.resources import GetMetricData
    metric_data = GetMetricData()
    output = metric_data.export()
    output.csv

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'fetch_all_rules': {
        'task': 'rule_engine.celery.fetch_all_rules',
        'schedule': crontab(minute="*/1"),
    },
    'generate_metric_data': {
            'task': 'rule_engine.celery.generate_metric_data',
            'schedule': crontab(minute="*/2"),
        },

}
