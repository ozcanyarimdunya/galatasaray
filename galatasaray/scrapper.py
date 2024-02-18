from datetime import date

import requests
from bs4 import BeautifulSoup


class Scraper:
    BASE_URL = "https://www.transfermarkt.com.tr"
    TEAM_ID = 141

    def __init__(self):
        self.session = self._initialize_session()
        self.soup = self._get_initial_soup()

    @staticmethod
    def _initialize_session():
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)"
                    " AppleWebKit/537.36 (KHTML, like Gecko)"
                    " Chrome/53.0.2785.143 Safari/537.36"
                ),
                "Accept-Encoding": "gzip, deflate",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        return session

    def _get_initial_soup(self):
        year = date.today().year - 1
        url = "{}/galatasaray-istanbul/startseite/verein/{}/saison_id/{}".format(self.BASE_URL, self.TEAM_ID, year)
        response = self.session.get(url)
        return BeautifulSoup(response.content, "html.parser")

    @property
    def matches(self):
        url = "{}/ceapi/nextMatches/team/{}".format(self.BASE_URL, self.TEAM_ID)
        return self.session.get(url).json()

    @property
    def rumors(self):
        url = "{}/ceapi/rumors/team/{}".format(self.BASE_URL, self.TEAM_ID)
        return self.session.get(url).json()["rumors"]

    @property
    def team_value(self):
        data = self.soup.select_one("a.data-header__market-value-wrapper")
        data.select_one("p").clear()
        return data.get_text(strip=True)

    @property
    def cups(self):
        return [
            [each.select_one("span").get_text(strip=True), each.get("title")]
            for each in self.soup.select(".data-header__badge-container a")
        ]

    @property
    def standings(self):
        standings = []
        table = self.soup.find("div", attrs={"data-viewport": "Tabelle"})
        for each in table.select("tbody tr"):
            n, _, c, m, a, p = each.select("td")
            row = [
                n.get_text(strip=True),  # no
                c.get_text(strip=True),  # club
                m.get_text(strip=True),  # matches
                a.get_text(strip=True),  # average
                p.get_text(strip=True),  # points
                "table-highlight" in each.attrs.get("class", [])  # highlight
            ]
            standings.append(row)

        return standings

    @property
    def truths(self):
        table = self.soup.find("div", attrs={"data-viewport": "Daten_und_Fakten"})
        truths = {
            "legal_name": table.find("span", attrs={"itemprop": "legalName"}).get_text(strip=True),
            "address": " ".join([i.get_text(strip=True) for i in table.find_all("div", attrs={"itemprop": "address"})]),
            "telephone": table.find("span", attrs={"itemprop": "telephone"}).get_text(strip=True),
            "fax": table.find("span", attrs={"itemprop": "faxNumber"}).get_text(strip=True),
            "url": table.find("span", attrs={"itemprop": "url"}).get_text(strip=True),
            "founded": table.find("span", attrs={"itemprop": "foundingDate"}).get_text(strip=True),
            "members": table.find("span", attrs={"itemprop": "member"}).get_text(strip=True)
        }
        return truths
