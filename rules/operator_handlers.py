import numpy as np
from rules import models

from common import date_time


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
        try:
            begin_time = date_time.modify_date_time(begin_time_given)
        except Exception as e:
            raise e
        metrics_list = models.MetricData.get_metric_data(metric_name=metric_name, begin_time=begin_time)

        if len(metrics_list) == 0:
            return "0"
        metrics_list = np.array(metrics_list)
        metrics_list_float = metrics_list.astype(np.float)
        result = np.percentile(metrics_list_float, 1)
        return str(result)


class AvgOperatorHandler(BaseOperatorHandler):
    def __init__(self, name):
        self.name = name
        BaseOperatorHandler.__init__(self, name)

    @property
    def description(self):
        return "gives average of the given field matrix"

    def evaluate(self, metric_name="time_taken", begin_time_given="0d_0h_0m_0s", *args, **kwargs):
        try:
            begin_time = date_time.modify_date_time(begin_time_given)
        except Exception as e:
            raise e
        metrics_list = models.MetricData.get_metric_data(metric_name, begin_time)
        if len(metrics_list) == 0:
            return "0"
        metrics_list = np.array(metrics_list)
        metrics_list_float = metrics_list.astype(np.float)
        result = np.average(metrics_list_float)
        return str(result)


operator_dictionary = {"avg": AvgOperatorHandler, "P99": P99OperatorHandler}
