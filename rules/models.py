from django.db import models
import sys
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

    def insert_into_rule_table(namespace_name, rule_condition, rule_name, frequency, logs):
        namespace_id = list(Namespace.objects.filter(name=namespace_name).values_list('id', flat=True))
        rule_object = Rule.objects.create(name=rule_name, namespace_id=namespace_id[0], frequency=frequency,
                                          rule_condition=rule_condition)
        if rule_object is None:
            logs.append("Error in creating " + rule_name + " " + namespace_name)
        return rule_object.pk

    def delete_rule(rule_id):
        Rule.objects.filter(id=rule_id).delete()

    def get_rule(rule_name):
        rules = list(Rule.objects.filter(name=rule_name))
        return rules

    def rule_existence(rule_name, namespace):
        rule_id = list(Rule.objects.filter(name=rule_name, namespace__name=namespace).values_list('id', flat=True))
        #print(rule_id)
        if len(rule_id) == 0:
            return None
        else:
            print(rule_id)
            return rule_id[0]

    def update(rule_id, namespace_name, rule_condition, rule_name, frequency):
        rule_object = Rule.objects.get(id=rule_id)
        rule_object.namespace__name = namespace_name
        rule_object.name = rule_name
        rule_object.frequency = frequency
        rule_object.rule_condition = rule_condition
        rule_object.save()

class Action(models.Model):
    name = models.CharField(max_length=100)
    action_type = action_type_choices
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def create_action(action_name, action_type):
        action_object = Action.objects.create(name=action_name, action_type=action_type)
        return action_object.pk

    def delete_action(action_id):
        Action.objects.filter(id=action_id).delete()

    def display(self, action_name):
        actions = list(Action.objects.filter(name=action_name))
        return actions

    def get_id_from_name(action_name, logs):
        print("ENTERED ")
        action_id = list(Action.objects.filter(name=action_name).values_list("id", flat=True))

        if action_id is None:
            logs.append(action_name + " not found")
        return action_id[0]


class RuleAction(models.Model):
    rule = models.ForeignKey(Rule, default=100, verbose_name="rule_id", on_delete=models.SET_DEFAULT)
    action = models.ForeignKey(Action, default=100, verbose_name="action_id", on_delete=models.SET_DEFAULT)
    value = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def insert_into_rule_action_table( rule_id, action_id, value, logs):
        rule_action = RuleAction.objects.create(rule_id=rule_id, action_id=action_id, value=value)
        if rule_action is None:
            logs.append("Error in creating row for " + value)

    def delete_rule_action(self, rule_id, action_id):
        RuleAction.objects.filter(rule_id=rule_id, action_id=action_id).delete()

    def display(self, rule_id, action_id):
        values = RuleAction.objects.filter(rule_id=rule_id, action_id=action_id)
        return list(values)


class ResponseTime(models.Model):
    #id = models.AutoField(primary_key=True)
    namespace = models.TextField()
    time_taken = models.IntegerField()
    response_code = models.IntegerField()
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.namespace

    def create_entry( namespace, time_taken, response_code, date_time):
        rule_action = ResponseTime.objects.create(namespace=namespace, time_taken=time_taken, response_code=response_code,
                                          date_time=date_time)

    def delete_entry(response_id):
        ResponseTime.objects.filter(id=response_id).delete()

    def get_columns(column_name, begin_time):
        print("models " + str(begin_time))
        print(list(ResponseTime.objects.filter(date_time__gte=str(begin_time)).values_list(column_name, flat=True)))
        return list(ResponseTime.objects.filter(date_time__gte=str(begin_time)).values_list(column_name, flat=True))



