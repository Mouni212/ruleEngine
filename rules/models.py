from django.db import models
from common.exceptions import exceptions

# Create your models here.

action_type_choices = (
    ("1", "slack"),
    ("2", "gmail"),
    ("3", "whatsapp"),
)


class Namespace(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    name = models.CharField(max_length=100)
    namespace = models.ForeignKey(Namespace, default=100, verbose_name="namespace", on_delete=models.SET_DEFAULT)
    frequency = models.IntegerField()
    rule_condition = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def insert_into_rule_table(namespace_name, rule_condition, rule_name, frequency):
        namespace_id = list(Namespace.objects.filter(name=namespace_name).values_list('id', flat=True))
        if len(namespace_id) == 0:
            raise exceptions.InvalidException("No entry found for " + str(namespace_name) + " in Namespace table")
        rule_object = Rule.objects.create(name=rule_name, namespace_id=namespace_id[0], frequency=frequency,
                                          rule_condition=rule_condition)
        if rule_object is None:
            raise exceptions.InvalidException("Error in creating " + rule_name + " " + str(namespace_name))
        else:
            return rule_object.pk

    def delete_rule(rule_id):
        Rule.objects.filter(id=rule_id).delete()

    def get_rule(rule_name):
        rules = list(Rule.objects.filter(name=rule_name))
        return rules

    def rule_existence(rule_name, namespace):
        rule_list = list(Rule.objects.filter(name=rule_name, namespace__name=namespace))
        i = 0
        while i < len(rule_list):
            if rule_list[i].is_active:
                return rule_list[i].id
            i = i+1
        return None

    def update(rule_id, rule_condition, frequency):
        rule_object = Rule.objects.get(id=rule_id)
        rule_object.frequency = frequency
        rule_object.rule_condition = rule_condition
        rule_object.is_active = True
        rule_object.save()


class Action(models.Model):
    name = models.CharField(max_length=100)
    action_type = action_type_choices
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def create_action(action_name, action_type):
        action_object = Action.objects.create(name=action_name, action_type=action_type)
        if action_object is None:
            raise exceptions.InvalidException("Error in creating " + action_name)
        else:
            return action_object.pk

    def delete_action(action_id):
        Action.objects.filter(id=action_id).delete()

    def get_actions(self, action_name):
        actions = list(Action.objects.filter(name=action_name))
        return actions

    def get_id_from_name(action_name):
        print("ENTERED ")
        action_id = list(Action.objects.filter(name=action_name).values_list("id", flat=True))

        if action_id is None:
            raise exceptions.InvalidException(action_name + " not found")
        return action_id[0]


class RuleAction(models.Model):
    rule = models.ForeignKey(Rule, default=100, verbose_name="rule_id", on_delete=models.SET_DEFAULT)
    action = models.ForeignKey(Action, default=100, verbose_name="action_id", on_delete=models.SET_DEFAULT)
    value = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def insert_into_rule_action_table( rule_id, action_id, value):
        rule_action = RuleAction.objects.create(rule_id=rule_id, action_id=action_id, value=value)
        if rule_action is None:
            raise exceptions.InvalidException("Error in creating row for " + value)

    def delete_rule_action(self, rule_id, action_id):
        RuleAction.objects.filter(rule_id=rule_id, action_id=action_id).delete()

    def get_rule_action(self, rule_id, action_id):
        values = RuleAction.objects.filter(rule_id=rule_id, action_id=action_id)
        return list(values)


class MetricData(models.Model):
    namespace = models.CharField(max_length=100)
    index = models.CharField(max_length=100)
    metric_value = models.CharField(max_length=100)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.namespace

    def create_entry( namespace, metric_name, metric_value, date_time):
        response_obj = MetricData.objects.create(namespace=namespace, index=metric_name, metric_value=metric_value,
                                          created_date=date_time)
        if response_obj is None:
            raise exceptions.InvalidException("Error in creating row for " + str(namespace))

    def delete_entry(metric_id):
        MetricData.objects.filter(id=metric_id).delete()

    def get_metric_data(metric_name, begin_time):
        return list(MetricData.objects.filter(created_date__gte=str(begin_time),
                                              index=metric_name).values_list('metric_value', flat=True))

