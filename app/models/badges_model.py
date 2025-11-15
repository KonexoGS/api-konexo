from dataclasses import dataclass

@dataclass
class Badge:
    _id: str
    name: str
    description: str
    required_experience: int
    how_to_get: str