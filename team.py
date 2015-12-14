class Team:
    def __init__(self, title=None, score=None, founder=None, member_count=None, year=None, team_type=None, location=None):
        self.title = title
        if score is None:
            self.score = 0
        else:
            self.score = score
        self.founder = founder
        if member_count is None:
            self.member_count = 0
        else:
            self.member_count = member_count
        self.team_type = team_type
        self.location = location
        if year is None:
            self.year = 0
        else:
            self.year = year
