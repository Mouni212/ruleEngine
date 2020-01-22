class Invalid(Exception):
    def __init__(self, message):
        print("Invalid {}".format(message))
