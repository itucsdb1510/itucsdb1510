class Basicmember:
    def __init__(self, name, surname, nickname, gender, email, password, byear, city, interests):
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.gender=gender
        self.email = email
        self.password=password
        self.byear = byear
        self.city=city
        self.interests= interests
        self.score=0
        self.membertype=0  #1 means professional user

