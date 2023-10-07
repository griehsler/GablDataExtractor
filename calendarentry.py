from datetime import date
from datetime import datetime

class CalendarEntry:
    town_id: int
    date: date
    kind: str
    rm: str
    p: str
    gs: str

    def __init__(self, town_id, date, kind, rm=None, p=None, gs=None):
        self.town_id = town_id
        self.date = datetime.strptime(date,'%d.%m.%Y')
        self.kind = kind
        self.rm = rm
        self.p = p
        self.gs = gs