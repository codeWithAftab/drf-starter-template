from exceptions.base import InvalidWeeklyOffList

def validate_weekly_off_list(weekly_off):
    if len(weekly_off) > 2:
        raise InvalidWeeklyOffList("Weeklyoff list can only contain 1 or 2 days.")