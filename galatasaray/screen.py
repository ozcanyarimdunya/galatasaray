from datetime import datetime
from time import sleep

from rich import box
from rich.align import Align
from rich.console import Console
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .scrapper import Scraper


class Application:
    def __init__(self):
        self.scrapper = Scraper()
        self.layout = Layout(name="root")
        self.layout.split(
            Layout(name="header", ratio=3),
            Layout(name="main", ratio=12),
            Layout(name="footer", ratio=1),
        )
        self.layout["header"].split_row(
            Layout(name="header-left", ratio=1),
            Layout(name="header-middle", ratio=3),
            Layout(name="header-right", ratio=1),
        )
        self.layout["main"].split_row(
            Layout(name="main-left", ratio=1),
            Layout(name="main-middle", ratio=1),
            Layout(name="main-right", ratio=1)
        )

    def setup(self):
        self.layout["header-left"].update(self.get_header_left())
        self.layout["header-middle"].update(self.get_header_middle())
        self.layout["header-right"].update(self.get_header_right())
        self.layout["main-left"].update(self.get_main_left())
        self.layout["main-middle"].update(self.get_main_middle())
        self.layout["main-right"].update(self.get_main_right())
        self.layout["footer"].update(self.get_footer())

    def run(self):
        with Live(self.layout, screen=True):
            while True:
                sleep(1)

    def get_header_left(self):
        cups = Table.grid(expand=True)
        cups.add_column(style="bold")
        cups.add_column()
        cups.add_column()
        for count, title in self.scrapper.cups:
            cups.add_row(count, " ", title)
        return Panel(Align.center(cups, vertical="middle"))

    @staticmethod
    def get_header_middle():
        logo = Group(
            Align.center(":star::star::star::star:\n"),
            Align.center("[red]GALATA[/red][yellow]SARAY[/yellow]\n"),
            Align.center("1905"),
        )
        return Panel(Align.center(logo, vertical="middle"), style="bold", padding=1)

    def get_header_right(self):
        return Panel(Align.center(f"Kadro değeri\n[b]{self.scrapper.team_value}[/b]", vertical="middle"))

    def get_main_left_top(self):
        standings = Table(expand=True, box=box.SIMPLE)
        standings.add_column(header="#")
        standings.add_column(header="Kulüp")
        standings.add_column(header="Maçlar")
        standings.add_column(header="+/-")
        standings.add_column(header="Puan")

        for no, club, matches, average, points, highlight in self.scrapper.standings:
            style = "u yellow on red" if highlight else None
            standings.add_row(no, club, matches, average, points, style=style)
        return Panel(standings, title="[cyan][b]TABLO KESİTİ SÜPER LİG[/b][/cyan]", box=box.SQUARE)

    def get_main_left_bottom(self):
        truths = Table.grid(expand=True)
        truths.add_column()
        truths.add_column()
        truths.add_column()
        tr = self.scrapper.truths
        truths.add_row("Resmi kulüp adı", ": ", tr["legal_name"])
        truths.add_row("Adres", ": ", tr["address"])
        truths.add_row("Tel", ": ", tr["telephone"])
        truths.add_row("Faks", ": ", tr["fax"])
        truths.add_row("Web sayfası", ": ", tr["url"])
        truths.add_row("Kuruluş", ": ", tr["founded"])
        truths.add_row("Üyeler", ": ", tr["members"])
        return Panel(truths, title="[cyan][b]VERİLER & GERÇEKLER[/b][cyan]", box=box.SQUARE)

    def get_main_left(self):
        left_top = self.get_main_left_top()
        left_bottom = self.get_main_left_bottom()
        return Panel(Group(left_top, left_bottom), box=box.SIMPLE)

    def get_main_middle(self):
        data = self.scrapper.matches

        next_matches = data["matches"][:6]
        items = []
        for each in next_matches:
            matches = Table.grid(expand=True)
            matches.add_column()
            matches.add_column(justify="center")
            matches.add_column()

            matches.add_row("", each["competition"]["label"], "")
            matches.add_row("", datetime.fromtimestamp(each["match"]["time"]).strftime("%d.%m.%Y %A - %H:%M"), "")
            matches.add_row(
                Align.left(data["teams"][str(each["match"]["home"])]["name"]),
                each["match"]["result"],
                Align.right(data["teams"][str(each["match"]["away"])]["name"]),
            )
            items.append(Panel(matches, padding=(0, 3), box=box.HORIZONTALS))

        return Panel(
            Panel(
                Group(*items),
                title="[cyan][b]SONRAKİ KARŞILAŞMALAR[/b][/cyan]"
            ),
            box=box.SIMPLE
        )

    def get_main_right(self):
        items = []
        for each in self.scrapper.rumors[:4]:
            rumors = Table.grid(expand=True)
            rumors.add_column()
            rumors.add_column(justify="center")
            rumors.add_column()
            rumors.add_row("", each["player"]["name"], "", style="bold")
            rumors.add_row("Yaş", ": ", str(each["player"]["age"]))
            rumors.add_row("Mevki", ": ", each["player"]["position"])
            rumors.add_row("Piyasa değeri", ": ", each["player"]["marketValue"])
            rumors.add_row(each["team1"]["name"], ">> ", each["team2"]["name"], style="bold italic")
            items.append(Panel(rumors, padding=(0, 3), box=box.HORIZONTALS), )
        return Panel(
            Panel(
                Group(*items),
                title="[cyan][b]GÜNCEL SÖYLENTİLER[/b][/cyan]"
            ),
            box=box.SIMPLE
        )

    @staticmethod
    def get_footer():
        table = Table.grid()
        table.add_column()
        table.add_column()
        table.add_column()
        table.add_row("quit", ": ", "CTRL + C")
        table.add_row("credit", ": ", Text("@ozcanyarimdunya", style="link https://yarimdunya.com"))
        return Panel(table, box=box.SIMPLE)


