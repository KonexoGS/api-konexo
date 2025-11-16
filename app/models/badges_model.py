from dataclasses import dataclass

@dataclass
class Badges:
    friendly_code: str
    name: str
    description: str
    required_experience: int
    how_to_get: str