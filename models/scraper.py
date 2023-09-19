from bs4 import BeautifulSoup
import requests
import json
from models import User, RecentSubmission
import concurrent.futures


class Scraper:
    def scrape_concurrently(self, users: [User]) -> None:
        """
        Scrape user profile information concurrently.

        :param users: list of LeetCode users
        :return: None
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            profiles = executor.map(self.scrape_user_profile, users)
            counter = 0
            for profile in profiles:
                users[counter].scraped_profile = profile
                counter += 1

    def scrape_user_profile(self, user: User) -> json:
        """
        Scrape user profile information.

        :param user: LeetCode user
        :return: LeetCode user information
        """
        print(f"Executing scrape for: {user.username}...")
        profile = "https://leetcode.com/" + user.username
        page = requests.get(profile)
        soup = BeautifulSoup(page.text, features="html.parser")
        return json.loads(soup.find('script', type="application/json").string)

    def filter_submission_calendar(self, data: json) -> list[dict]:
        """
        Filter data to find submission calendar.

        :param data: LeetCode user information
        :return: parsed submission calendar data as a list of dictionaries
        """
        submission_calendar = json.loads(data["props"]["pageProps"][
                                               "dehydratedState"]["queries"][7][
                                               "state"]["data"]["matchedUser"][
                                               "userCalendar"][
                                              "submissionCalendar"])
        return [{int(i): v} for i, v in submission_calendar.items()]

    def filter_recent_submissions(self, user) -> list[RecentSubmission]:
        """
        Filter data to find user's recent submissions.

        :param user: LeetCode user
        :return: parsed recent submission data as a list of RecentSubmission
        """
        if user.username != user.scraped_profile["query"]["username"]:
            print("Data does not match User provided.")
        recent_submissions = user.scraped_profile["props"]["pageProps"]["dehydratedState"][
            "queries"][6]["state"]["data"]["recentAcSubmissionList"]
        return [RecentSubmission(submission["id"], submission["title"], submission[
            "titleSlug"], int(submission["timestamp"]), user) for submission in
                recent_submissions]
