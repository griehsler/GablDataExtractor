import re
import html.parser
from CalendarEntry import CalendarEntry
from Town import Town

class GablHtmlParser(html.parser.HTMLParser):

    def __init__(self):
        self.inEntry = False
        self.entries = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.inEntry = False
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'tunterlegt':
                    self.inEntry = True

    def handle_endtag(self, tag):
        self.inEntry = False

    def handle_data(self, data):
        if self.inEntry:
            self.entries.append(data.strip())
            

_regex1 = r"\w{2}\s+(?P<date>[0-9\.]+)\s+(?P<kind>.+)((\s+in Zone \w+ Gebiet\s+RM\s+(?P<RM>\w+)[\s/]+Papier\s+(?P<P>\w+)[\s/]+LV\s+(?P<GS>\w+)))"
_regex2 = r"\w{2}\s+(?P<date>[0-9\.]+)\s+(?P<kind>.+)"

def parseCalendarEntry(gemeinde, line):
    match = re.search(_regex1, line)
    if match != None:
        return CalendarEntry(gemeinde, match.group("date"), match.group('kind'), match.group('RM'), match.group('P'), match.group('GS'))
    else:
        match = re.search(_regex2, line)
        return CalendarEntry(gemeinde, match.group("date"), match.group('kind'))

_townRegex = r"<a href=\"\?gem_nr=(?P<id>\d+)[^>]+>(?P<name>[^<^,]+)[^<]*<"

def parseTowns(pageText):
    matches = re.findall(_townRegex, pageText)
    return list(map(lambda match: Town(match[0], match[1]), matches))