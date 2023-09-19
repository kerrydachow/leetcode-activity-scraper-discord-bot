from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass(eq=False)
class User:
    """
    Class for keeping track of recent submission
    """
    username: str
    scraped_profile: Optional[json] = field(default=None, repr=False)

    def __eq__(self, other) -> bool:
        """
        Configure equals method to compare the username of User.

        :param other: other user
        :return: bool
        """
        if not isinstance(other, User):
            return False
        return self.username == other.username
