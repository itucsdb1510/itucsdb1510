from tkinter import Place
class Team:
    def __init__(self, title=None, score=None, founder=None, year=None):
        self.title = title
        if score is None:
            self.score = 0
        else:
            self.score = score
        self.founder = founder
        self.members = founder
        self.member_count = 1
        if year is None:
            self.year = 0
        else:
            self.year = year