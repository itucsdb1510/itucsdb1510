import datetime

class Topic:
    def __init__(self, title, text, time):
        now = datetime.datetime.now()
        self.title=title
        self.text=text
        self.time=now
