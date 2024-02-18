from galatasaray.screen import Application


def main():
    """
    Main function
    :return: None
    """
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(ex)
