class Admin:
    def __init__(self, lunch_tray_height, lunch_tray_length):
        self.lunch_tray_height = lunch_tray_height
        self.lunch_tray_length = lunch_tray_length

    def to_dict(self):
        return {
            'lunch_tray_height': self.lunch_tray_height,
            'lunch_tray_length': self.lunch_tray_length
        }

    @staticmethod
    def from_dict(data):
        return Admin(
            lunch_tray_height=data.get('lunch_tray_height', 0),
            lunch_tray_length=data.get('lunch_tray_length', 0)
        ) 