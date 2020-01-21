from django.db import models

# Create your models here.


class ActionManager(models.Manager):
    def create_action(self, action_name, action_type):
        action_object = self.objects.create(name=action_name, type=action_type)
        return action_object.pk

    def delete_action(self, action_id):
        self.objects.filter(id=action_id).delete()

    def display(self, action_name):
        actions = self.objects.filter(name=action_name)
        return actions

    def get_id_from_name(self, action_name, logs):
        action = self.objects.get(name=action_name)
        if action is None:
            logs.append(action_name + " not found")
        return action.action_id


class RuleManager(models.Manager):
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


class RuleActionManager(models.Manager):
    def insert_into_rule_action_table(self, rule_id, action_id, url, logs):
        rule_action = self.objects.create(rule_id=rule_id, action_id=action_id, url=url)
        if rule_action is None:
            logs.append("Error in creating row for " + url)

    def delete_rule_action(self, rule_id, action_id):
        self.objects.filter(rule_id=rule_id, action_id=action_id).delete()

    def display(self, rule_id, action_id):
        urls = self.objects.filter(rule_id=rule_id, action_id=action_id)
        return urls


class ResponseTimeManager(models.Manager):
    def create_entry(self, namespace, time_taken, response_code, date_time):
        rule_action = self.objects.create(namespace=namespace, time_taken=time_taken, response_code=response_code,
                                          date_time=date_time)

    def delete_entry(self, response_id):
        self.objects.filter(id=response_id).delete()

    def get_columns(self, column_name, begin_time):
        urls = self.objects.filter(date_time__gte=begin_time)
        return getattr(urls, column_name)


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
    rule = models.TextField()
    is_active = models.BooleanField(default=True)
    rule = RuleManager()

    def __str__(self):
        return self.name


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    type = models.TextField()
    is_active = models.BooleanField(default=True)
    action = ActionManager()

    def __str__(self):
        return self.id


class RuleAction(models.Model):
    id = models.AutoField(primary_key=True)
    rule_id = models.ForeignKey(Rule, default=0, verbose_name="rule_id", on_delete=models.SET_DEFAULT)
    action_id = models.ForeignKey(Action, default=0, verbose_name="action_id", on_delete=models.SET_DEFAULT)
    url = models.TextField()
    is_active = models.BooleanField(default=True)
    rule_action = RuleActionManager()

    def __str__(self):
        return self.id


class ResponseTime(models.Model):
    id = models.AutoField(primary_key=True)
    namespace = models.TextField()
    time_taken = models.IntegerField()
    response_code = models.IntegerField()
    date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    response_time = ResponseTimeManager()

    def __str__(self):
        return self.namespace



