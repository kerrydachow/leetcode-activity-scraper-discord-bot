from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class User:
    """
    Class for keeping track of recent submission
    """
    username: str
    scraped_profile: Optional[json] = field(default=None, repr=False)
