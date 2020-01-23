import requests
import jsondef post_to_slack(url,msg):
 data = {'text': msg}
 response = requests.post(url, json.dumps(data), headers={'content-type': 'application/json'})
 return responseurl= 'https://hooks.slack.com/services/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'
msg= 'Hi! This is a bot built by Rishabh.'
r = post_to_slack(url,msg)
print(r.text+" "+str(r.status_code))