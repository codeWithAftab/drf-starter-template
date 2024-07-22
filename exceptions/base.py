from django.conf import settings 

class InvalidWeeklyOffList(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
