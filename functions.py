#file: functions.py
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
    while True:
        line = input(">> ")
        if line == "\end":
            return 0

        line_processed = line + "\n"
        try:
            with open(file_path, "a") as f:
                f.write(line_processed)
        except Exception as e:
            print(e)
            return 1
        continue

def load_save(save_file, char_id):
    os.environ['LOADED_SAVE'] = str(id)
    save_file_ex = os.path.abspath(save_file)
    all_saves = load_data(save_file_ex)

    game_section = all_saves[char_id["game_section"]]

    os.system(f"python3 section_{game_section}")