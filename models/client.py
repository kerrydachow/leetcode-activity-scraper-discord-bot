from .user import User
from .scraper import Scraper
from datetime import datetime


class Client:
    """
    Client to execute requests to scrape.
    """
    _instance = None

    def __init__(self):
        """
        Initialize with an instance of a scraper & users list.
        """
        self.users = []
        self.scraper = Scraper()

    def __new__(cls):
        """
        Implement Singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            return cls._instance

    def execute_request(self, request, username=None) -> None | list:
        """
        Execute the given request.

        :param request: user request
        :param username: username if specified
        :return: None or executed request information
        """
        match request:
            case 1:
                self.scraper.scrape_concurrently(self.users)
                return
            case 2:
                return self._get_users_list_last_submission_info()
            case 3:
                return self._get_user_last_submission_info(username)
            case _:
                print("Invalid input")
                return

    def add_user(self, username) -> bool:
        """
        Add a user to client's list of users.

        :param username: LeetCode username
        :return: boolean
        """
        user = User(username)
        if user not in self.users:
            self.users.append(User(username))
            return True
        else:
            return False

    def remove_user(self, username) -> bool:
        """
        Remove a user from client's list of users.

        :param username: LeetCode username
        :return: boolean
        """
        user = User(username)
        if user in self.users:
            self.users.remove(User(username))
            return True
        else:
            return False

    def get_users(self) -> list[str]:
        """
        Return list of client's users as usernames.

        :return: list of client's users as usernames
        """
        return [user.username for user in self.users]

    def _get_user_last_submission_info(self, username) -> list[str | dict]:
        """
        Get user's last submissions.

        :param username: LeetCode username
        :return: user's last submissions
        """
        user = User(username)
        user.scraped_profile = self.scraper.scrape_user_profile(user)
        submissions = self.scraper.filter_recent_submissions(user)
        result = [f"{user.username}'s recent submissions were:"]
        submission_dict = {}
        for submission in submissions:
            submission_dict[submission.title] = f"@ {datetime.fromtimestamp(submission.timestamp).strftime('%Y-%m-%d %I:%M:%S %p')}"
        result.append(submission_dict)
        return result

    def _get_users_list_last_submission_info(self) -> list[list[str | dict]]:
        """
        Get client's list of users' last submissions.

        :return: list of user's last submissions
        """
        output = []
        for user in self.users:
            if user.scraped_profile:
                submissions = self.scraper.filter_recent_submissions(user)
                result = [f"{user.username}'s recent submissions were:"]
                submission_dict = {}
                for submission in submissions:
                    submission_dict[submission.title] = f"@ {datetime.fromtimestamp(submission.timestamp).strftime('%Y-%m-%d %I:%M:%S %p')}"
                result.append(submission_dict)
                output.append(result)
        return output
