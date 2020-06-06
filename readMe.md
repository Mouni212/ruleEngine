# Monitoring and Alerting Engine

There are millions of requests to some services every minute.
To manually check traffic, resource utilisation and other parameters for any system to ensure it's smooth functioning are an essential but a gigantic task. 
We need a service to track our systems and services' health. It has to monitor if the parameters of the system are within the threshold. 
 We have developed a service which can track any system's health when provided with thresholds and conditions. 
Now comes the next problem; request rate may change, and thresholds may change, and we can even face a security attack. For that, we have used state of the art machine learning algorithm to identify abnormal behaviour to reconfigure our thresholds or identify potential attacks in future.

This service allows for monitoring of multiple systems. Each system's health can be measured using certain system parameters.  If it exceed certain limits then the person incharge will be alerted say on slack. Feed it exact conditions and it will check in background which parameters break threshold and alert you. This service also runs anomaly detection to see abbreation in the concerned parameter  like response time in the case of DDoS attack. 

Slides are also attached to understand the use case.

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
