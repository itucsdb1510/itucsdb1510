class Basicmember:
    def __init__(self, name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role):
        self.name = name
        self.surname = surname
        self.username = username
        self.gender=gender
        self.email = email
        self.password=password
        self.byear = byear
        self.city=city
        self.interests= interests
        self.score=0
        self.award_G=0
        self.award_S=0
        self.award_B=0
        self.membertype=0  #0 means basic member
        self.lastlogin = lastlogin
        self.regtime = regtime
        self.role = role

