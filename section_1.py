#File: section_1.py
#Written by: Angelo Semertsidis
#License: GNU GPLv3
#Year: 2025

import functions as funcs
import os
import time

save_data_file = "./data/save_data.json"
game_data_file =  "./data/game_data.json"

# Loading character data
char_id = os.environ.get('LOADED_SAVE')
if not char_id:
    char_id = "1"
_, fname, lname, race, char_class, gender, game_section = funcs.load_save_data(char_id, save_data_file)
_, pers_pronoun, poss_pronoun_1, poss_pronoun_2, obj_pronoun = funcs.pronouns(gender)
full_name = f"{fname} {lname}".title()
print("="*100)
print(f"\ncharacter id: {char_id}\npronouns: {pers_pronoun}, {poss_pronoun_1}, {poss_pronoun_2}, {obj_pronoun}\
      \nfirst name: {fname}\nlast name: {lname}\nrace: {race}\nclass: {char_class}")
