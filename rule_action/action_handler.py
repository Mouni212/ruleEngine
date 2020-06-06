import requests, json

class ActionHandler:
    def __init__(self):
        pass

    @property
    def description(self):
        pass

    def apply_action(url, msg):
        pass


class SlackHandler(ActionHandler):
    def __init__(self):
        ActionHandler.__init__(self)

    @property
    def description(self):
        return "posts the message to slack"

    @classmethod
    def apply_action(cls, url, msg):
        print("In apply action")
        print(msg)
        data = {'text': msg}
        print(data['text'])
        response = requests.post(url, json.dumps(data), headers={'content-type': 'application/json'})
        return response

action_dictionary = {"slack": SlackHandler}