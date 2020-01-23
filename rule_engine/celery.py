from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rule_engine.settings')
app = Celery('rule_engine')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
CELERY_TIMEZONE = 'UTC'


app.autodiscover_tasks()


@app.task(name="rule_evaluator")
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
                handler.apply_action('https://hooks.slack.com/services/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', msg=rule.name + " state is now ALARM")
    return

@app.task(name="schedule_rules")
def fetch_all_rules():
    from rule_action import action_handler
    from rule_action.action_handler import action_dictionary
    from rules import utils
    from rules.models import RuleAction, Rule

    active_rule_list = list(Rule.objects.filter(is_active=True).values_list('id', flat=True))
    print((active_rule_list))
    for rule_id in active_rule_list:
        evaluate(rule_id)

'''
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-min-time': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}'''

