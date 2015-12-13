import datetime

class Topic:
    def __init__(self, title, text, time, categoryId):
        now = datetime.datetime.now()
        self.title=title
        self.text=text
        self.time=time
        self.categoryId=categoryId
