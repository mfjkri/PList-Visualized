from names_extractor import get_names_that_matches_participants
from ui import UI

present_participants_dict = get_names_that_matches_participants()
# matched_registered = list(present_participants_dict.keys())
# matched_registered.sort()


ui = UI(1920, 1080)
ui.start(present_participants_dict)
