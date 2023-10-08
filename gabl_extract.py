import gablhtmlparser
import download
import logging
import os
from jsonserialize import serializeCalendarEntries
from regionsconfig import add_regions

logging.basicConfig(format='%(message)s', level=20)

def get_towns(regions):
    logging.info("downloading towns overview...")
    page_text = download.get_towns_page()
    towns = gablhtmlparser.parseTowns(page_text)
    logging.info("downloaded towns overview.")
    add_regions(towns, regions)
    return towns

def get_town_entries(gemeinde_ids):
    entries = []
    gablparser = gablhtmlparser.GablHtmlParser()
    for gemeinde_id in gemeinde_ids:
        logging.info(f"downloading town calendar of {gemeinde_id}...")
        gablparser.feed(download.get_entries_page(gemeinde_id))
        new_entries = list(map(lambda line: gablhtmlparser.parseCalendarEntry(gemeinde_id, line), gablparser.entries))
        logging.info(f"downloaded town calendar of {gemeinde_id}.")
        entries.extend(new_entries)

    return entries

def store_entries(filename, entries):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(serializeCalendarEntries(entries))

def store_pdf(filename, content):
    with open(filename, mode="wb") as file:
        file.write(content)

def extract_towns_and_calendars():
    towns = get_towns("regions.json")
    store_entries("towns.json", towns)
    town_ids = list(map(lambda town: town.town_id, towns))
    calendars = get_town_entries(town_ids)
    store_entries("calendar.json", calendars)

def extract_all_pdfs(year):
    towns = get_towns("regions.json")
    town_ids = list(map(lambda town: town.town_id, towns))
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")
    for town_id in town_ids:
        logging.info(f"downloading town pdf of {town_id}...")
        store_pdf(os.path.join("pdfs", f"{town_id}.pdf"), download.get_pdf(year, town_id))
        logging.info(f"downloaded town pdf of {town_id}.")

extract_towns_and_calendars()
#extract_all_pdfs(2023)
