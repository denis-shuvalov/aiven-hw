import sys
from app import app


def run():
    app.start()


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run()
