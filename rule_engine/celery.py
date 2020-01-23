from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from rules.monitoring import validate_evaluate
from rule_action import action_handler
from models import RuleAction

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rule_engine.settings')
app = Celery('rule_engine')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(name="rule_evaluator")
def evaluate(rule_id):
    rule = Rule.objects.get(rule_id, is_active=True);
    result = validate_evaluate(rule)

    if result is not None:
        rule_actions = list(RuleAction.objects.get(rule_id=rule_id).value_list('action__name', 'value', flat=True))

        for rule_action in rule_actions:
            handler = action_dictionary.get(rule_action.action)
            if handler is not None:
                handler.apply_action(rule_action.value, msg = rule.rule_name+" state is now ALARM")
    return

@app.task(name="schedule_rules")
def fetch_all_rules():
    active_rule_list = list(Rule.objects.get(is_active=True));
    for rule in active_rule_list:
        evaluate(rule.id)
      #  evaluate.delay(args=[rule.rule_id], kwargs={}, countdown=rule.frequency)
      #  Monitoring.validate_evaluate.delay(args=[rule, logs], kwargs={}, countdown=rule.frequency)

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-min-time': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
