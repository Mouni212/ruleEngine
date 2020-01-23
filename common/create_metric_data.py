from rules.models import MetricData

metric_data = [["Recommendation", "Response_time", "25", '2019-01-01 00:00:00.000000'],
               ["Recommendation", "Response_time", "48", '2025-05-27 05:10:19.189474'],
               ["Recommendation", "Response_time", "45", '2020-01-22 05:39:18.765887'],
               ["Recommendation", "Response_time", "145", '2030-11-17 15:35:29.344474'],
               ["Recommendation", "Response_time", "21", '2020-01-23 04:45:56.749785']]


def metric_data_table():
    for data in metric_data:
        MetricData.create_entry(data[0], data[1], data[2], data[3])
