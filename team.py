class Team:
    def __init__(self, title, score, founder, year=None):
        self.title = title
        self.score = score
        self.founder = founder
        self.members = founder
        self.member_count = 1
        self.year = year