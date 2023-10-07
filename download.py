import requests

_base_address = "https://bruck.umweltverbaende.at"

def _create_url(town_id, category):
    address = f"{_base_address}/?kat={category}"
    if town_id is not None:
        address = address + f"&gem_nr={town_id}"
    return address

def _fetch_page(town_id, category=32):
    http_page = requests.get(_create_url(town_id, category))
    return http_page.text

def get_entries_page(town_id):
    return _fetch_page(town_id)

def get_towns_page():
    return _fetch_page(None)
