from __future__ import absolute_import

import datetime
import os
import random

from celery import Celery
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
    if result is not None:
        rule_actions = list(RuleAction.objects.filter(id=rule_id).values_list('action__name', 'value'))
        for rule_action in rule_actions:
            handler = action_dictionary.get(rule_action[0])
            if handler is not None:
                # handler.apply_action(rule_action[1], msg=rule.name+" state is now ALARM")
                handler.apply_action('https://hooks.slack.com/services/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',
                                     msg=rule.name + " state is now ALARM")
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


@app.task(queue='celery')
def generate_metric_data(initial_date=datetime.datetime(2015, 5, 27, 12, 4, 5),
                         current_date=datetime.datetime(2015, 5, 27, 12, 4, 5)):
    from rules.models import MetricData
    current_date = current_date + datetime.timedelta(date=1)

    metric_low_range = 100
    metric_high_range = 200
    days = (current_date - initial_date).days
    if 100 < days < 200:
        metric_low_range = 300
        metric_high_range = 400
    MetricData.create_entry(random.choice(namespace_list), random.choice(metric_index_list),
                            random.randrange(metric_low_range, metric_high_range, 10), current_date)


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'fetch_all_rules': {
        'task': 'rule_engine.celery.fetch_all_rules',
        'schedule': 1,
    },
    'generate_metric_data': {
            'task': 'rule_engine.celery.generate_metric_data',
            'schedule': 3,
        },

}
