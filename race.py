class Race:
    def __init__(self, title, race_type, founder, time, place):
        self.title = title
        self.race_type = race_type
        self.founder = founder
        self.time = time
        self.place = place
        self.participants = founder
        self.participant_count = 1