from enum import Enum

def convert_enums_to_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
        elif isinstance(value, list):
            data[key] = [v.value if isinstance(v, Enum) else v for v in value]
    return data