import gablhtmlparser
import download
from calendarentry import CalendarEntry
from jsonserialize import serializeCalendarEntries

def get_towns():
    page_text = download.get_towns_page()
    towns = gablhtmlparser.parseTowns(page_text)
    return towns

def get_town_entries(gemeinde_ids):
    entries = []
    gablparser = gablhtmlparser.GablHtmlParser()
    for gemeinde_id in gemeinde_ids:
        gablparser.feed(download.get_entries_page(gemeinde_id))
        new_entries = list(map(lambda line: gablhtmlparser.parseCalendarEntry(gemeinde_id, line), gablparser.entries))
        entries.extend(new_entries)

    return entries

def store_entries(filename, entries):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(serializeCalendarEntries(entries))

def store_pdf(filename, content):
    with open(filename, mode="wb") as file:
        file.write(content)

def extract_towns_and_calendars():
    towns = get_towns()
    store_entries("towns.json", towns)
    town_ids = list(map(lambda town: town.town_id, towns))
    calendars = get_town_entries(town_ids)
    store_entries("calendar.json", calendars)

def extract_all_pdfs(year):
    towns = get_towns()
    town_ids = list(map(lambda town: town.town_id, towns))
    for town_id in town_ids:
        store_pdf(f"pdfs\\{town_id}.pdf", download.get_pdf(year, town_id))

extract_towns_and_calendars()
#extract_all_pdfs(2023)
