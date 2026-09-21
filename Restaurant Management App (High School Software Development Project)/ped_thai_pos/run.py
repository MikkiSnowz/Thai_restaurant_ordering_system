"""Start the Ped Thai Cuisine POS:  python run.py"""
import sys

if sys.version_info < (3, 10):
    sys.exit("Ped Thai POS needs Python 3.10 or newer.")

from pos.db import Database
from pos.ui.app import App


def main():
    App(Database()).run()


if __name__ == "__main__":
    main()
