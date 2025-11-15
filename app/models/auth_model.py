from dataclasses import dataclass
from pydantic import NaiveDatetime

@dataclass
class Auth():
    dev_id: str
    token: str
    created_at: NaiveDatetime
    