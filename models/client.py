from .user import User
from .scraper import Scraper
from datetime import datetime


class Client:
    _instance = None

    def __init__(self):
        self.users = []
        self.scraper = Scraper()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            return cls._instance

    def execute_request(self, request):
        match request:
            case 1:
                self.scraper.scrape_concurrently(self.users)
                return
            case 2:
                self._print_last_submission_info()
                return
            case _:
                print("Invalid input")
                return

    def add_user(self, username):
        self.users.append(User(username))

    def _print_last_submission_info(self):
        for user in self.users:
            if user.scraped_profile:
                results = self.scraper.filter_recent_submissions(user)
                print(f"{user.username}'s recent submissions were:")
                for submission in results:
                    print(f"{submission.title :<80} @ "
                          f"{datetime.fromtimestamp(submission.timestamp).strftime('%Y-%m-%d %I:%M:%S %p')}")
                print()
            else:
                print("Must scrape profile first!\n")
