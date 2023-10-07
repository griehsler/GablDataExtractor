import parser
import download
from calendarentry import CalendarEntry
from jsonserialize import serializeCalendarEntries

def get_towns():
    page_text = download.get_towns_page()
    towns = parser.parseTowns(page_text)
    return towns

def get_town_entries(gemeinde_ids):
    gablparser = parser.GablHtmlParser()
    for gemeinde_id in gemeinde_ids:
        gablparser.feed(download.get_entries_page(gemeinde_id))

    entries = list(map(lambda line: parser.parseCalendarEntry(gemeinde_id, line), gablparser.entries))
    return entries

def store_entries(filename, entries):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(serializeCalendarEntries(entries))

towns = get_towns()
store_entries("towns.json", towns)
town_ids = list(map(lambda town: town.town_id, towns))
calendars = get_town_entries(town_ids)
store_entries("calendar.json", calendars)
