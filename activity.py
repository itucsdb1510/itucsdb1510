class Activity:
    def __init__(self, title, activity_type, founder, time, place):
        self.title = title
        self.activity_type = activity_type
        self.founder = founder
        self.time = time
        self.place = place
        self.participants = founder
        self.participant_count = 1