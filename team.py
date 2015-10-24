class Team:
    def __init__(self, title, score, founder, members, member_count, year=None):
        self.title = title
        self.score = score
        self.founder = founder
        self.members = members
        self.member_count = member_count
        self.year = year