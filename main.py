#file: main.py
#Written by: Angelo Semertsidis
#License: GNU GPLv3
#Year: 2025

import functions as funcs
import os

save_data_file = "./data/save_data.json"
game_data_file =  "./data/game_data.json"

try:
    result, game_data = funcs.load_data(game_data_file) # Loads game data from file
    print("\n** WELCOME TO MIDDLE EARTH! **\n")

    start_action_choices = ["New save", "Load save", "Exit"]

    for i, name in enumerate(start_action_choices, 1):
        print(f"{i}. {name}")

    while True: #Error loop for invalid action selections
        try:
            start_action = int(input("Choose an action (number): "))
            break
        except ValueError:
            print("ERROR: Please enter a valid number to start!")
            continue

    # New Save
    if start_action == 1:
        result, save_data = funcs.load_data(save_data_file)

        char_id = len(save_data) + 1

        fname = input("\nEnter your character's first name: ")
        lname = input("\nEnter your character's last name: ")
        print()
        
        race_options = ["Dwarf", "Elf", "Hobbit", "Human", "Orc"]
        for i, name in enumerate(race_options, 1):
            print(f"{i}. {name}")
        race = int(input("Please choose a race (number): "))

        print()
        char_class_options = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Rogue', 'Wizard']
        for i, name in enumerate(char_class_options, 1):
            print(f"{i}. {name}")
        char_class = int(input("Please choose a class (number): "))

        gender = input("\nChoose a gender (optional): ")
        if gender == "":
            gender = None

        if game_data["unlocked_areas"] == None:
            game_section = 1
        else:
            while True:
                game_section = int(input(f"\nChoose starting section (1-{game_data['unlocked_areas']}): "))

                if game_section > game_data["unlocked_areas"]:
                    print("ERROR: You haven't unlocked that level!")
                    continue
                elif game_section < 1:
                    print("ERROR: Invalid level!")
                    continue

                break

        new_save = funcs.new_save(save_data_file, char_id ,fname, lname, race, char_class, game_section, gender)
        if new_save == 0:
            start_now_query = input("\nSuccessfully made new save! Would you like to start now? (Y/n) ").lower()
            if start_now_query == "" or start_now_query == "y":
                funcs.load_save(save_data_file, char_id)
            else:
                exit("\nBye :)\n")
        
    # Load save
    elif start_action == 2:
        result, save_data = funcs.load_data(save_data_file)

        if not save_data or save_data == "{}":
            print("ERROR: No saves found!")
            exit()
        else:
            print()
            for key, character in save_data.items():
                full_name = f"{character['fname']} {character['lname']}".title()
                print(f"{key}. {full_name}")

            while True:
                selected_save = input("\nSelect a save (number): ")
                if selected_save in save_data:
                    funcs.load_save(save_data_file, selected_save)
                    break
                else:
                    print("ERROR: Invalid save selection!")
                    continue
            
            funcs.load_save(save_data_file, selected_save)

    # Exit game
    elif start_action == 3:
        exit("\nBye! Come back soon!\n")

except KeyboardInterrupt:
    exit("\n\nBye :)\n")
