import json
from datetime import date

def serializeCalendarEntries(entries):
    return json.dumps(entries, default=_json_default, indent=2)

def _json_default(value):
    if isinstance(value, date):
        return f"{value.year}{value.month:02d}{value.day:02d}"
    else:
        return value.__dict__