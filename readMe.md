# Monitoring and Alerting Engine

This service allows for monitoring of multiple systems. Each system's health can be measured in parameter. FOr example, server health can be measured with response time. If it exceed certain limits we alert you, say on slack. We can use this service in similar manner. Feed it exact conditions and it will check in background which parameters break threshold and alert you. After that this service also runs anomaly detection to see if the response time or considered parameter as gone up unusually like in case of DDoS attack. In that case, you have to take precautions.
Slides are also attached.

One such request to server can be:
```
{
  "name": "Rule4",
  "namespace": "Recommendation",
  "frequency":"0d_0h_0m_5000s",
  "rule_condition": "P99 time_taken 0d_0h_0m_0s > -5",
  "actions":[{"name": "slack", "value": "https://hooks.slack.com/services/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"},
	{"name": "gmail", "value": "hv"}
  	]
} 
```
### Alarm message for above query on data in Real time query database

![](AlertOnSlack.png)

### Anomaly Detection Code 

![](anomaly_detection_sample_result.png)

### Incoming real time data on MySQL in Grafana

![](grafana_ruleEngine.png)

## Contributors

- Rishabh Gupta
- Mounika Mukkamalla
## Python command
- python manage.py runserver
## Celery commands
 - celery worker -A rule_engine -Q celery
 - celery beat -A rule_engine
 
#### Mentored by Vikas Chahal, Unacademy
