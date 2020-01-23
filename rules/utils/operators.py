import numpy as np
from rules import models

from rules.utils import date_time


class BaseOperatorHandler:
    def __init__(self, name):
        self.name = name

    @property
    def description(self):
        pass

    def evaluate(self, metric_name="time_taken", begin_time_given="0d_0h_0m_0s"):
        pass


class P99OperatorHandler(BaseOperatorHandler):
    def __init__(self, name):
        self.name = name
        BaseOperatorHandler.__init__(self, name)

    @property
    def description(self):
        return "gives worst 1% of the given field matrix"

    def evaluate(self, metric_name="time_taken", begin_time_given="0d_0h_0m_0s"):
        begin_time = date_time.modify_date_time(begin_time_given)
        column_name_list = models.ResponseTime.get_metric_data(metric_name=metric_name, begin_time=begin_time)
        if len(column_name_list) == 0:
            return "0"
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

    def evaluate(self, metric_name="time_taken", begin_time_given="0d_0h_0m_0s", *args, **kwargs):
        begin_time = date_time.modify_date_time(begin_time_given)
        metric_list = models.ResponseTime.get_metric_data(metric_name, begin_time)
        if len(metric_list) == 0:
            return "0"
        metric_list = np.array(metric_list)
        result = np.average(metric_list)
        return str(result)


operator_dictionary = {"avg": AvgOperatorHandler, "P99": P99OperatorHandler}
