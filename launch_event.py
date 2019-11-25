import mission as ms
import requests
import re
from lxml import html


class LaunchEvents:
    missions = []

    def __init__(self):
        url = "https://everydayastronaut.com/prelaunch-previews/"
        page = requests.get(url)
        page_content = html.fromstring(page.content)

        tale_rows = page_content.xpath('//tr')
        i = 0

        for row in tale_rows:
            string = row.text_content()
            if len(string) > 200:
                data = string.split("|")
                mission_name = data[0] + "|" + data[1]
                mission_name = mission_name.split()
                mission_name = " ".join(sorted(set(mission_name), key=mission_name.index))

                location = re.findall("Location(.*)LSP", string)[0].strip()
                lsp = re.findall("LSP(.*)Rocket", string)[0].strip()
                rocket = mission_name.split("|")[0].strip()

                window_start = re.findall("Window start(.*)UTCWindow", string)[0].strip()
                window_end = re.findall("Window end(.*)UTC", string)[0].strip()

                start_date = re.findall("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", window_start)[0]
                start_time = re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", window_start)[0]
                end_time = re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", window_end)[0]

                mission = ms.Mission(mission_name, location, lsp, rocket, start_date, start_time, end_time)
                self.missions.append(mission)
            elif string.strip() == "Mission NameDate and Time" and i > 1:
                break
            i += 1
