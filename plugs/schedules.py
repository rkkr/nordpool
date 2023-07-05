from datetime import datetime

class Schedules:
    def get_state(prices):
        pass

class FixedTimeOn(Schedules):
    def __init__(self, hour_from, hour_to):
        self.hour_from = hour_from
        self.hour_to = hour_to

    def get_state(self, prices):
        now = datetime.now().hour
        return now >= self.hour_from and now < self.hour_to

class FixedTimeOff(FixedTimeOn):
    def get_state(self, prices):
        return not super().get_state(prices)
