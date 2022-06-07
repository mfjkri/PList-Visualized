import os
import yaml

from typing import (Union, Any)
from src.names_extractor import get_names_that_matches_participants
# from src.ui import UI


PARTICIPANTS_FILE = os.path.join("participants.yaml")

# ui = UI(1920, 1080)
# ui.start(present_participants_dict)


def load_yaml_file(file_path: str) -> Union[Any, bool]:
    assert os.path.isfile(file_path), f"No file found at {file_path}"

    with open(file_path, 'r') as stream:
        config = {}
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            config = False
            print(exception)
        return config


def updated_attendee_txt(present_participants_dict: dict) -> None:

    attendees_json = os.path.join("PlistWeb", "attendees.json")

    matched_registered = list(present_participants_dict.keys())

    print("Matched participants:", len(matched_registered))

    matched_registered.sort()

    file_lines = ["{\n"]
    idx = 0

    for name in matched_registered:
        matched_names: list = present_participants_dict[name]
        file_lines.append(f"""\t"{name}": [\n""")
        file_lines.append(f"""\t\t"  ",\n""")

        for matched_name in matched_names:
            file_lines.append(f"""\t\t"{matched_name}",\n""")

        file_lines[-1] = file_lines[-1][:-2] + "\n"
        file_lines.append(f"""\t],\n""")

    file_lines[-1] = file_lines[-1][:-2] + "\n"
    file_lines.append("}")
    with open(attendees_json, 'w') as stream:
        stream.writelines(file_lines)


if __name__ == "__main__":
    participants = load_yaml_file(PARTICIPANTS_FILE)
    present_participants_dict = get_names_that_matches_participants(
        participants)
    updated_attendee_txt(present_participants_dict)
