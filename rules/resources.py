from import_export import resources
from .models import MetricData


class GetMetricData(resources.ModelResource):
    class Meta:
        model = MetricData
        fields = ('created_date', 'metric_value')
