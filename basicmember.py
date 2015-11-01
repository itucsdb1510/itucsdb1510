class Basicmember:
    def __init__(self, name, surname, nickname, email, password, byear, city, interests):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.email = email
        self.password=password
        self.byear = byear
        self.city=city
        self.interests= interests
        self.award_G=0
        self.award_S=0
        self.award_B=0
        self.score=0
        self.membertype=0  #1 means professional user
        self.messages=0
        self.events=0
        self.basicmember_count = 1
