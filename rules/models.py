from django.db import models
import sys
# Create your models here.


class Namespace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    namespace_id = models.ForeignKey(Namespace, default=0, verbose_name="namespace_id", on_delete=models.SET_DEFAULT)
    frequency = models.IntegerField()
    rule = models.TextField(default="10>20")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def insert_into_rule_table(self, namespace_name, rule, rule_name, frequency, logs):
        namespace_id = Namespace.objects.get(name=namespace_name)
        rule_object = self.objects.create(rule_name=rule_name, namespace_id=namespace_id, frequency=frequency,
                                          rule=rule)
        if rule_object is None:
            logs.append("Error in creating " + rule_name + " " + namespace_name)

        return rule_object.pk

    def delete_rule(self, rule_id):
        self.objects.filter(rule_id=rule_id).delete()

    def get_rule(self, rule_name):
        rules = self.objects.filter(rule_name=rule_name)
        return rules


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    type = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def create_action(action_name, action_type):
        action_object = Action.objects.create(name=action_name, type=action_type)
        return action_object.pk

    def delete_action(action_id):
        Action.objects.filter(id=action_id).delete()

    def display(self, action_name):
        actions = Action.objects.filter(name=action_name)
        return actions

    def get_id_from_name(action_name, logs):
        action = Action.objects.get(name=action_name)
        if action is None:
            logs.append(action_name + " not found")
        return action.action_id


class RuleAction(models.Model):
    id = models.AutoField(primary_key=True)
    rule_id = models.ForeignKey(Rule, default=0, verbose_name="rule_id", on_delete=models.SET_DEFAULT)
    action_id = models.ForeignKey(Action, default=0, verbose_name="action_id", on_delete=models.SET_DEFAULT)
    url = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def insert_into_rule_action_table( rule_id, action_id, url, logs):
        rule_action = RuleAction.objects.create(rule_id=rule_id, action_id=action_id, url=url)
        if rule_action is None:
            logs.append("Error in creating row for " + url)

    def delete_rule_action(self, rule_id, action_id):
        RuleAction.objects.filter(rule_id=rule_id, action_id=action_id).delete()

    def display(self, rule_id, action_id):
        urls = RuleAction.objects.filter(rule_id=rule_id, action_id=action_id)
        return urls

'''
class ResponseTimeManager(models.Manager):
    def get_columns(self, column_name, begin_time):
        print("models " + str(begin_time))
        urls = ResponseTime.objects.filter(date_time__gte=begin_time)
        return getattr(urls, column_name)

'''
class ResponseTime(models.Model):
    id = models.AutoField(primary_key=True)
    namespace = models.TextField()
    time_taken = models.IntegerField()
    response_code = models.IntegerField()
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        self.__getattribute__(e)
        return self.namespace


    def __getattribute__(self, item):


    def create_entry( namespace, time_taken, response_code, date_time):
        rule_action = ResponseTime.objects.create(namespace=namespace, time_taken=time_taken, response_code=response_code,
                                          date_time=date_time)

    def delete_entry(response_id):
        ResponseTime.objects.filter(id=response_id).delete()

    def get_columns(column_name, begin_time):
        print("models " + str(begin_time))
        response_time_obj = ResponseTime.objects.filter(date_time__gte=str(begin_time))
        column_attr = getattr(sys.modules[__name__], column_name)
        return



