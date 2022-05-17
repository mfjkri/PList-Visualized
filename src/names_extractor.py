import os
from bs4 import BeautifulSoup

PLIST_DIR = os.path.join("PlistHtml")
PLIST_FILE_NAMES = os.listdir(PLIST_DIR)


def get_names_that_matches_participants(participants: list) -> dict:

    attendees_set = set()

    for plist_file_name in PLIST_FILE_NAMES:
        plist_file = os.path.join(PLIST_DIR, plist_file_name)

        if os.path.isfile(plist_file):
            with open(plist_file, 'r') as stream:
                html_soup = BeautifulSoup(stream, features="html.parser")

                [attendees_set.add(tag.string) for tag in html_soup.find_all(
                    class_="style-title-2qhbq")]

    attendees_list = list(attendees_set)
    attendees_list.sort()

    present_participants_dict = {}

    for participant in participants:
        name_segments = participant.split(' ')

        for segment in name_segments:
            if len(segment) > 3:
                for attendee in attendees_list:
                    if segment.lower() in attendee.lower():
                        present_participants_dict[participant].add(
                            attendee
                        ) if participant in present_participants_dict else present_participants_dict.update(
                            {participant: set([attendee])}
                        )

    for participant, _ in present_participants_dict.items():
        present_participants_dict[participant] = list(
            present_participants_dict[participant])
        present_participants_dict[participant].sort()

    return present_participants_dict
