#File: functions.py
#Written by: Angelo Semertsidis
#License: GNU GPLv3
#Year: 2025

import json
import os
import sys
from functools import wraps

error_codes = {
    1: "Unkown or Unexpected error",
    2: "JSON decoder error",
    3: "File not found"
}

# Error listener to give the correct codes when error is produced by a funciton
def error_listener(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, int) and result in error_codes:
            print(f"ERROR: {result}: {error_codes[result]}")
            print(f"Error occured in function: {func.__name__}")
            sys.exit(result)
        
        return result
    return wrapper

# Loads game data from game data file (default: game_data.json)
@error_listener
def load_data(path):
    file_path = os.path.abspath(path)
    try:
        with open(file_path, "r") as data:
            game_data = json.load(data)

        return 0, game_data
    except FileNotFoundError:
        return 3, None
    except json.JSONDecodeError:
        return 2, None
    except Exception as e:
        print(e)
        return 1, None

# Creates a new character/save in the save data file (default: save_data.json)
@error_listener
def new_save(save_path, id, fname, lname, race, char_class, game_section, gender):
    file_path = os.path.abspath(save_path)

    new_save = {
        id: {
            "fname": fname,
            "lname": lname,
            "race": race,
            "class": char_class,
            "gender": gender,
            "game_section": game_section
        }
    }
    
    try:
        with open(file_path, "r") as f:
            content_check = f.read()
        

        if not content_check:
            try:
                with open(file_path, "w") as save_data:
                    json.dump(new_save, save_data, indent=4)

                return 0
            except FileNotFoundError:
                return 3
            except Exception as e:
                print(e)
                return 1
        else:
            try:
                with open(file_path, "r") as all_saves:
                    all_saves_loaded = json.load(all_saves)

                all_saves_loaded.update(new_save)
            except FileNotFoundError:
                return 3
            except json.JSONDecodeError:
                return 2
            except Exception as e:
                print(e)
                return 1
            
            try:
                with open(file_path, "w") as save_data:
                    json.dump(all_saves_loaded, save_data, indent=4)
                
                return 0
            except FileNotFoundError:
                return 3
            except Exception as e:
                print(e)
                return 1
    except FileNotFoundError:
        return 3
    except json.JSONDecodeError:
        return 2
    except Exception as e:
        print(e)
        return 1

@error_listener
def writer(path):
    file_path = os.path.abspath(path)

    def del_line(filename, line_number_to_delete):
        with open(filename, "r") as f:
            lines = f.readlines()

        index_to_delete = line_number_to_delete - 1 

        with open(filename, "w") as f:
            for index, line in enumerate(lines):
                if index != index_to_delete:
                    f.write(line)

    def printer(path):
        file_path = os.path.abspath(path)
        try:
            with open(file_path, "r") as f:
                for line in f:
                    print(line, end="")
        except FileNotFoundError:
            return 3
        except Exception as e:
            print(e)
            return 1

    while True:
        line = input(f"[{path}] >> ")

        # Commands in the text writer
        if line == "\end": # Exit text writer
            return 0
        elif line == "--print" or line == "-p": # Print whole file
            printer(path)
            continue
        elif "--delete" in line or "-d" in line: # Delete line
            _, ln = line.split()

            if ln.lower() == "a": # Delete entire contents of file
                with open(file_path, "w") as f:
                    f.seek(0)
                    f.truncate()
                continue
            del_line(file_path, int(ln))
            continue
        elif line == "":
            continue

        line_processed = line + "\n"
        try:
            with open(file_path, "a") as f:
                f.write(line_processed)
        except Exception as e:
            print(e)
            return 1
        continue

def load_save(save_file, char_id):
    os.environ['LOADED_SAVE'] = str(char_id)
    save_file_ex = os.path.abspath(save_file)
    _, all_saves = load_data(save_file_ex)

    char_data = all_saves[char_id]
    game_section = char_data["game_section"]

    os.system(f"python3 section_{game_section}.py")

def load_save_data(char_id, path):
    _, all_char_data = load_data(path)

    char_data = all_char_data[char_id]

    fname = char_data["fname"]
    lname = char_data["lname"]
    race = char_data["race"]
    char_class = char_data["class"]
    gender = char_data["gender"]
    game_section = char_data["game_section"]

    return 0, fname, lname, race, char_class, gender, game_section

def pronouns(gender):
    if gender == None:
        pers_pronoun = "they"
        poss_pronoun_1 = "their"
        poss_pronoun_2 = "theirs"
        obj_pronoun = "them"
    elif gender.lower() == "m":
        pers_pronoun = "he"
        poss_pronoun_1 = "his"
        poss_pronoun_2 = "his"
        obj_pronoun = "him"
    elif gender.lower() == "f":
        pers_pronoun = "she"
        poss_pronoun_1 = "hers"
        poss_pronoun_2 = "hers"
        obj_pronoun = "her"
    else:
        pers_pronoun = "they"
        poss_pronoun_1 = "their"
        poss_pronoun_2 = "theirs"
        obj_pronoun = "them"

    return 0, pers_pronoun, poss_pronoun_1, poss_pronoun_2, obj_pronoun
