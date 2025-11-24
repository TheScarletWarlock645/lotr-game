#file: main.py
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
def load_game_data(path):
    file_path = os.path.abspath(path)
    try:
        with open(file_path, "r") as data:
            game_data = json.load(data)

        return 0, game_data
    except FileNotFoundError:
        return 3, None
    except json.JSONDecodeError:
        return 2, None
    except Exception:
        return 1, None

# Creates a new character/save in the save data file (default: save_data.json)
@error_listener
def new_save(path, fname, lname, race, game_section, gender=None):
    file_path = os.path.abspath(path)
    char_name = f"{fname} {lname}".title()

    try:
        with open(file_path, "r") as f:
            content_check = f.read()
        
        if not content_check:
            new_save = {
                char_name: {
                    "fname": fname,
                    "lname": lname,
                    "race": race,
                    "gender": gender,
                    "game_section": game_section
                }
            }

            try:
                with open(file_path, "w") as save_data:
                    json.dump(new_save, save_data, indent=4)
            except FileNotFoundError:
                return 3, file_path, None
            except Exception as e:
                return 1, None, e

        new_save = {
            char_name: {
                "fname": fname,
                "lname": lname,
                "race": race,
                "gender": gender,
                "game_section": game_section
            }
        }

        try:
            with open(file_path, "r") as all_saves:
                all_saves_loaded = json.load(all_saves)

            all_saves_loaded.append(new_save)
            
        except FileNotFoundError:
            return 3
        except json.JSONDecodeError as e:
            return 2
        except Exception as e:
            return 1
        
        try:
            with open(file_path, "w") as f:
                content_check = f.read()

                if not content_check:
                    
                else:
                    json.dump(all_saves_loaded, f, indent=4)

     