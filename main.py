from app import OKXOrbitApp


def main():
    app = OKXOrbitApp()
    app.server.start(port=8081, open_browser=True)


if __name__ == "__main__":
    main()
