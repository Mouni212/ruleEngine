import datetime
import numpy as np
from rules import models
import sys

from rules.utils import date_time


def str_to_class(class_name):
    return getattr(sys.modules[__name__], class_name)


class BaseOperatorHandler:
    def __init__(self, name):
        self.name = name

    @property
    def description(self):
        pass

    def evaluate(self, column_name="time_taken", begin_time_given="0d 0h 0m 0s", *args, **kwargs):
        begin_time = date_time.change_date_time(begin_time_given)
        pass


class P99OperatorHandler(BaseOperatorHandler):
    def __init__(self, name):
        self.name = name
        BaseOperatorHandler.__init__(self, name)

    @property
    def description(self):
        return "gives worst 1% of the given field matrix"

    def evaluate(self, column_name="time_taken", begin_time_given="0d 0h 0m 0s"):
        begin_time = date_time.change_date_time(begin_time_given)
        print("YEAH WE ARE IN EVALUATE")
        print("operators " + str(begin_time))
        column_name_list = models.ResponseTime.get_columns(column_name=column_name, begin_time=begin_time)
        print(column_name_list)
        column_name_list = np.array(column_name_list)
        result = np.percentile(column_name_list, 1)
        return str(result)


class AvgOperatorHandler(BaseOperatorHandler):
    def __init__(self, name):
        self.name = name
        BaseOperatorHandler.__init__(self, name)

    @property
    def description(self):
        return "gives average of the given field matrix"

    def evaluate(self, column_name="time_taken", begin_time_given="0d 0h 0m 0s", *args, **kwargs):
        begin_time = date_time.change_date_time(begin_time_given)
        column_name_list = models.ResponseTime.get_columns(column_name, begin_time)
        column_name_list = np.array(column_name_list)
        result = np.percentile(column_name_list, 1)
        return str(result)


operator_dictionary = {"avg": "AvgOperatorHandler", "P99": "P99OperatorHandler"}
