from bs4 import BeautifulSoup
import requests
import json
from models import User, RecentSubmission


def scrape_user_profile(user: User):
    """
    Scrape user profile information.

    :param user: LeetCode user
    :return: LeetCode user information
    """
    profile = "https://leetcode.com/" + user.username
    page = requests.get(profile)
    soup = BeautifulSoup(page.text, features="html.parser")
    return json.loads(soup.find('script', type="application/json").string)


def filter_submission_calendar(data: json):
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


def filter_recent_submissions(data: json, user: User):
    """
    Filter data to find user's recent submissions.

    :param data: LeetCode user information
    :param user: LeetCode user
    :return: parsed recent submission data as a list of RecentSubmission
    """
    if user.username != data["query"]["username"]:
        print("Data does not match User provided.")
    recent_submissions = data["props"]["pageProps"]["dehydratedState"][
        "queries"][6]["state"]["data"]["recentAcSubmissionList"]
    return [RecentSubmission(submission["id"], submission["title"], submission[
        "titleSlug"], int(submission["timestamp"]), user) for submission in
            recent_submissions]
