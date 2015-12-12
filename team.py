class Team:
    def __init__(self, title=None, score=None, founder=None, year=None, team_type=None, location=None):
        self.title = title
        if score is None:
            self.score = 0
        else:
            self.score = score
        self.founder = founder
        self.members = founder
        self.member_count = 1
        self.team_type = team_type
        self.location = location
        if year is None:
            self.year = 0
        else:
            self.year = year

    def image_path(self, _id=None):
        if _id==None and self._id==None:
            return url_for('static',filename='.') + 'image/teams/not_available.png'
        if _id:
            return url_for('static',filename='.') + 'image/teams/' + str(_id) + '.png'
        else:
            return url_for('static',filename='.') +'image/teams/' + str(self._id) + '.png'
