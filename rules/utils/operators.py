import datetime
import numpy as np
from rules import models


class BaseOperatorHandler:
    def __init__(self, name):
        self.name = name

    @property
    def description(self):
        pass

    def evaluate(self, column_name="TimeTaken", begin_time=datetime.timedelta(), *args, **kwargs):
        pass


class P99OperatorHandler(BaseOperatorHandler):
    def __init__(self, name):
        self.name = name
        BaseOperatorHandler.__init__(self, name)

    @property
    def description(self):
        return "gives worst 1% of the given field matrix"

    def evaluate(self, column_name="TimeTaken", begin_time=datetime.timedelta()):
        column_name_list = models.ResponseTime.objects.get_columns(column_name, begin_time)
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

    def evaluate(self, column_name="TimeTaken", begin_time=datetime.timedelta(), *args, **kwargs):
        column_name_list = models.ResponseTime.objects.get_columns(column_name, begin_time)
        column_name_list = np.array(column_name_list)
        result = np.percentile(column_name_list, 1)
        return str(result)


operator_dictionary = {"avg": "AvgOperatorHandler", "P99": "P99OperatorHandler"}
