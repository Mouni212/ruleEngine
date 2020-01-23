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
        data = {'text': msg}
        response = requests.post(url, json.dumps(data), headers={'content-type': 'application/json'})
        return response

action_dictionary = {"slack": SlackHandler}