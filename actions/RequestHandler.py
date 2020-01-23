
class RequestHandler:
    def __init__(self):
        pass

    @property
    def description(self):
        pass

    def request(url, msg):
        pass

class PostToSlack(RequestHandler):
    def __init__(self):
        RequestHandler.__init__(self)

    @property
    def description(self):
        return "posts the message to slack"

    def request(url, msg):
        data = {'text': msg}
        response = requests.post(url, json.dumps(data), headers={'content-type': 'application/json'})
        return response


