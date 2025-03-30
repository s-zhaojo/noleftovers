class User:
    def __init__(self, uuid, name, points, no_of_lunches_today, no_of_submissions_today):
        self.uuid = uuid
        self.name = name
        self.points = points
        self.no_of_lunches_today = no_of_lunches_today
        self.no_of_submissions_today = no_of_submissions_today

    def get_uuid(self):
        return self.uuid
    
    def get_name(self):
        return self.name
    
    def get_points(self):
        return self.points
    
    def get_no_of_lunches_today(self):
        return self.no_of_lunches_today
    
    def get_no_of_submissions_today(self):
        return self.no_of_submissions_today