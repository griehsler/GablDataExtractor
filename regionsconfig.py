import json
from collections import defaultdict
from Region import Region

from Regional import Regional

def add_regions(towns, regions):
    region_details = _load_regions(regions)
    for town in towns:
        if town.town_id in region_details:
            for name, flags in region_details[town.town_id].items():
                town.add_region(Region(name, flags.rm, flags.p, flags.gs))

def _load_regions(regions):
    f = open(regions) 
    inputdata = json.load(f)
    data = _transpose(inputdata)
    return data

def _transpose(loadeddata):
    result = {}
    for d in loadeddata:
        regions = defaultdict(Regional)
        _transpose_sub(regions, d, 'rm')
        _transpose_sub(regions, d, 'p')
        _transpose_sub(regions, d, 'gs')
        result[d['town_id']] = dict(regions)
    return result

def _transpose_sub(dict, entries, kind):
    for entry in entries[kind]:
        value = entry['value']
        regions = entry['regions']
        for region in regions:
            setattr(dict[region], kind, value)
