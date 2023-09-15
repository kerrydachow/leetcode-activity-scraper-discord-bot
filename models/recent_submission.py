from dataclasses import dataclass
from .user import User


@dataclass
class RecentSubmission:
    """
    Class for keeping track of recent submission
    """
    id: int
    title: str
    title_slug: str
    timestamp: int
    user: User
