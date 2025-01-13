from dataclasses import dataclass
from typing import List

DAYS_OF_THE_WEEK = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


@dataclass
class Date:
    day_of_week: str
    hour: int
    minute: int


@dataclass
class Medicine:
    name: str
    when_to_take: List[Date]
    pills_count: float  # float because maybe sometimes half a pill should be taken

@dataclass
class Event:
    def __init__(self, day: int, month: str, year: int, hour: int, minute: int, content: str, reminders: list):
        self.date = datetime(year, datetime.strptime(month, '%B').month, day, hour, minute)
        self.content = content
        self.reminders = reminders  # List to store multiple reminders

    def __str__(self):
        return f"{self.content} on {self.date.strftime('%B %d, %Y at %H:%M')}"

@dataclass
class Reminder:
    def __init__(self, event: Event, days_before: int = 0, hours_before: int = 0, minutes_before: int = 0):
        self.event = event
        self.reminder_time = event.date - timedelta(days=days_before, hours=hours_before, minutes=minutes_before)


