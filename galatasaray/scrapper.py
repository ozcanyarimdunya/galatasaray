import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/39.0.2171.95 Safari/537.36 "
            }
        )

        response = self.session.get(
            url="https://www.transfermarkt.com.tr/galatasaray-istanbul/startseite/verein/141/saison_id/2022"
        )
        self.soup = BeautifulSoup(response.content, "html.parser")

    @property
    def matches(self):
        return self.session.get("https://www.transfermarkt.com.tr/ceapi/nextMatches/team/141").json()

    @property
    def rumors(self):
        return self.session.get("https://www.transfermarkt.com.tr/ceapi/rumors/team/141").json()["rumors"]

    @property
    def team_value(self):
        data = self.soup.select_one("a.data-header__market-value-wrapper")
        data.select_one("p").clear()
        return data.get_text(strip=True)

    @property
    def cups(self):
        cups = []
        for each in self.soup.select(".data-header__badge-container a"):
            cups.append(
                [
                    each.select_one("span").get_text(strip=True),
                    each.get("title"),
                ]
            )
        return cups

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
