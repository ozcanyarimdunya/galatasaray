from .screen import Application


def main():
    try:
        screen = Application()
        screen.setup()
        screen.run()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(ex)
