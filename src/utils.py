import webbrowser


def open_link(url: str):
    def open():
        webbrowser.open(url)

    return open
