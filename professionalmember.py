class Professionalmember:
    def __init__(self, name, surname, username,gender, email, password, byear, city,interests, award_G,award_B, award_S,lastlogin, regtime, role):
        self.name = name
        self.surname = surname
        self.username = username
        self.gender=gender
        self.email = email
        self.password=password
        self.byear = byear
        self.city=city
        self.interests = interests
        self.award_G=award_G
        self.award_S=award_S
        self.award_B=award_B
        self.score=0
        self.teamid=0
        self.membertype=1  #1 means professional user
        self.lastlogin = lastlogin
        self.regtime = regtime
        self.role = role