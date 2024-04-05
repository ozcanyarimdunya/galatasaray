import argparse
from importlib import metadata

from galatasaray.screen import Application


def main():
    """The main entry point of the application."""
    parser = argparse.ArgumentParser(prog="galatasaray", description="Everything about the Galatasaray from cli!")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=metadata.version("galatasaray"),
        help="show version and exit.",
    )
    parser.parse_args()

    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(ex)
