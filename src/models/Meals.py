class Meal:
    def __init__(self, userId, date_taken, pts):
        self.userId = userId
        self.date_taken = date_taken
        self.pts = pts

    def to_dict(self):
        return {
            'userId': self.userId,
            'date_taken': self.date_taken,
            'pts': self.pts
        }

    @staticmethod
    def from_dict(data):
        return Meal(data['userId'], data['date_taken'], data['pts'])
