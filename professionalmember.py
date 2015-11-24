class Professionalmember:
    def __init__(self, name, surname, nickname,gender, email, password, byear, city,interests, award_G,award_B, award_S):
        self.name = name
        self.surname = surname
        self.nickname = nickname
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
        self.membertype=1  #1 means professional user