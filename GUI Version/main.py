# necessary imports:
import random
import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog
import tkinter.ttk as ttk
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import sys
from Units import Warrior, Tanker

# global variables:
# user_units will store user units
user_units = []
# aiUnits will store AI units
aiUnits = []
# character_frame_components will store all the labels etc of a user unit
character_frame_components = []
# ai_frame_components will store all the labels etc of an AI unit
ai_frame_components = []


# necessary functions:

# Create three user-controlled units
def CreatePlayerUnit():
    # input name and type of unit 3 times
    for i in range(3):
        print(f"Unit {i + 1}:")
        # input name and type of unit
        name = input("Enter Name for the unit:")
        unit_type = input("Enter 'w' for Warrior or 't' for Tanker: ")
        # create unit based on input
        if unit_type == 'w':
            unit = Warrior()
            unit.name = name
            user_units.append(unit)
        elif unit_type == 't':
            unit = Tanker()
            unit.name = name
            user_units.append(unit)
        else:
            print("Invalid input. Please enter 'w' or 't'.")
            print("Please try again.")
            print("Quitting")
            break
    print("User-controlled units:")
    # print out the units
    for unit in user_units:
        print(
            f" Name: {unit.name}, Health Point: {unit.health_point}, Attack Point: {unit.attack_point}, Defense Point: {unit.defense_point}, Experience Point: {unit.experience_point}, Rank: {unit.rank}")

# Create three AI-controlled units


def CreateAiUnit():
    # list which stores the random numbers of the units
    random_numbers = []
    # create three units
    for i in range(3):
        # randomly choose a type of unit
        unit_type = random.choice(['w', 't'])
        random_number = random.randint(1, 100)
        # make sure the random number is not repeated
        while random_number in random_numbers:
            random_number = random_number + 1
        # assign the random number to the unit
        name = "Ai:" + str(random_number)
        # add unit to the list
        if unit_type == 'w':
            unit = Warrior()
            unit.name = name
            aiUnits.append(unit)
        elif unit_type == 't':
            unit = Tanker()
            unit.name = name
            aiUnits.append(unit)


# function to display the player unit attributes on the gui
def CreateCharacterFrame():
    try:
        # using a for loop
        for i in range(0, 3):
            # create a frame for each unit
            individual_frame = tk.Frame(
                game_frame, width=game_width/4, height=game_width/2, )
            # check if the unit is a warrior or a tanker
            isWarrior = True
            if user_units[i].__class__.__name__ == "Tanker":
                isWarrior = False
            if isWarrior:
                image = Image.open("warrior.jpg")
            else:
                image = Image.open("tanker.jpg")
            # resize image
            image = image.resize((80, 80), Image.ANTIALIAS)
            # name of the unit
            name = tk.Label(
                individual_frame, text=f"{user_units[i].name}", font=("Arial", 10, "bold"))
            # style for the health bar
            style = ttk.Style()
            style.theme_use('default')
            style.configure("custom.Horizontal.TProgressbar",
                            background='#0f7504')
            # all required labels:
            character_health_bar = ttk.Progressbar(
                individual_frame, style="custom.Horizontal.TProgressbar", orient="horizontal", length=100, mode="determinate")
            character_image = ImageTk.PhotoImage(image)
            character_image_label = tk.Label(
                individual_frame, image=character_image)
            character_image_label.image = character_image
            attack_button = tk.Button(
                individual_frame, text="Attack", command=lambda index=i: AttackAiUnit(index), bg="#050373", fg='white')
            health_button = tk.Button(
                individual_frame, text="Heal", fg='white',  bg="#0f7504", command=lambda index=i: HealUserUnit(index))
            # displaying all the info using grid manager
            name.grid(row=0, column=1)
            character_health_bar.grid(row=0, column=0)
            character_image_label.grid(row=1, column=0, pady=5, rowspan=2)
            character_health_bar["value"] = user_units[i].health_point
            attack_button.grid(row=1, column=1, pady=5)
            health_button.grid(row=2, column=1, pady=5)
            # storing all the info in a dictionary
            my_dict = {}
            my_dict["name"] = name
            my_dict["image"] = character_image_label
            my_dict["attack"] = attack_button
            my_dict["health"] = health_button
            my_dict["frame"] = individual_frame
            my_dict["health_bar"] = character_health_bar
            # append the dictionary in character_frame_components
            character_frame_components.append(my_dict)
    except:
        print("Please press the create units button first to create the units.")
        print("Quitting")
        sys.exit()


# function to display AI units
def CreateAiFrame():
    # using a for loop
    for i in range(0, 3):
        # create a frame for each unit
        individual_frame = tk.Frame(
            game_frame, width=game_width/4, height=game_width/2)
        # check if the unit is a warrior or a tanker
        isWarrior = True
        if aiUnits[i].__class__.__name__ == "Tanker":
            isWarrior = False
        if isWarrior:
            image = Image.open("warrior.jpg")
        else:
            image = Image.open("tanker.jpg")
        image = image.resize((80, 80), Image.ANTIALIAS)
        # necessary labels
        name = tk.Label(individual_frame,
                        text=f"{aiUnits[i].name}", font=("Arial", 10, "bold"))
        style = ttk.Style()
        style.theme_use('default')
        style.configure("custom.Horizontal.TProgressbar", background='#0f7504')
        character_health_bar = ttk.Progressbar(
            individual_frame, style='custom.Horizontal.TProgressbar', orient="horizontal", length=100, mode="determinate")
        character_image = ImageTk.PhotoImage(image)
        character_image_label = tk.Label(
            individual_frame, image=character_image)
        character_image_label.image = character_image
        # displaying all the info using grid manager
        name.grid(row=0, column=0)
        character_health_bar.grid(row=1, column=0)
        character_image_label.grid(row=2, column=0)
        character_health_bar["value"] = aiUnits[i].health_point
        # storing all the info in a dictionary
        my_dict = {}
        my_dict["name"] = name
        my_dict["image"] = character_image_label
        my_dict["frame"] = individual_frame
        my_dict["health_bar"] = character_health_bar
        ai_frame_components.append(my_dict)


# function which is called when the attack button is clicked
def AttackAiUnit(index):
    # create a new window to ask for the enemy unit
    option_window = tk.Toplevel(root)
    option_window.title("Choose an AI unit to attack")
    option_window.geometry("300x300")
    enemy_list = tk.Listbox(option_window)
    label = tk.Label(option_window, text=index)
    # checking if the enemy is already dead or not
    for i in range(0, 3):
        if aiUnits[i].health_point > 0:
            enemy_list.insert(i, aiUnits[i].name)
        else:
            enemy_list.insert(i, f"{aiUnits[i].name} (Dead)")
    # function which is called when a particular enemy is selected

    def get_selected_enemy():
        # get the selected enemy

        selected_enemy = enemy_list.curselection()[0]

        selected_unit = aiUnits[selected_enemy]

        # check if the unit attacking is already dead or not
        if user_units[index].health_point > 0 and selected_unit.health_point > 0:
            logs = []
            # calculating damage using the formula given in the requirements
            damage = user_units[index].attack_point - \
                selected_unit.defense_point + random.randint(-5, 10)
            # decreasing the health of the enemy
            selected_unit.health_point -= damage
            # appending experience
            user_units[index].experience_point += damage
            def_exp = selected_unit.defense_point
            if damage > 10:
                def_exp = def_exp + def_exp*0.2
            if damage <= 0:
                def_exp = def_exp + def_exp*0.5
            selected_unit.experience_point += def_exp
            # appending rank
            if (selected_unit.experience_point >= 100):
                selected_unit.experience_point = selected_unit.experience_point - 100
                selected_unit.rank = selected_unit.rank + 1
            if (user_units[index].experience_point >= 100):
                user_units[index].experience_point = user_units[index].experience_point - 100
                user_units[index].rank = user_units[index].rank + 1
            ai_frame_components[selected_enemy]["health_bar"]["value"] = selected_unit.health_point
            # adding all the necessary information in logs
            logs.append(
                f'{user_units[index].name} attacked {selected_unit.name} for {damage} damage!')
            logs.append(
                f'{selected_unit.name} has {selected_unit.health_point} health left!')
            logs.append(
                f'{selected_unit.name} has {selected_unit.experience_point} experience points!')
            logs.append(f'{selected_unit.name} is rank {selected_unit.rank}!')
            logs.append(
                f'{user_units[index].name} has {user_units[index].experience_point} experience points!')
            logs.append(
                f'{user_units[index].name} is rank {user_units[index].rank}!')
            if selected_unit.health_point <= 0:
                logs.append(f'{selected_unit.name} has died!')
            option_window.destroy()
            CheckWinner()
            # adding log information to the game log and the log file
            for log in logs:
                try:
                    AddToGamelog(log)
                    AddToLogfile(log)
                except:
                    pass
            AttackCharacterUnit()

        else:
            logs = []
            if user_units[index].health_point <= 0:
                logs.append(
                    f'{user_units[index].name} is already dead! so he cannot attack!')
            if selected_unit.health_point <= 0:
                logs.append(
                    f'{selected_unit.name} is already dead! so he cannot be attacked!')
            option_window.destroy()
            for log in logs:
                try:
                    AddToGamelog(log)
                    AddToLogfile(log)
                except:
                    pass

    confirm_button = tk.Button(
        option_window, text="Confirm", command=get_selected_enemy)
    enemy_list.pack()
    confirm_button.pack()


# function which is used to add information to the game log
def AddToGamelog(text):
    gamelog.insert(tk.END, text + "\n")
    gamelog.see(tk.END)

# function to heal user units


def HealUserUnit(index):
    # checking the unit is already dead or not
    if user_units[index].health_point > 0:
        # if it is not dead then find its rank and heal it
        logs = []
        rank = user_units[index].rank
        second_wind = 0
        # if rank is greater than 1 then heal it
        if rank > 1:
            # calculate healed health
            second_wind = second_wind + 100*rank*0.2
            user_units[index].health_point = user_units[index].health_point + second_wind
            user_units[index].rank = user_units[index].rank - 1
            # append those points
            if user_units[index].health_point > 100:
                user_units[index].health_point = 100
            logs.append(
                f'{user_units[index].name} healed, present health is {user_units[index].health_point}!')
            # display the health bar
            character_frame_components[index]["health_bar"]["value"] = user_units[index].health_point
            # add the logs to the game log and the log file
            for log in logs:
                try:
                    AddToGamelog(log)
                    AddToLogfile(log)
                except:
                    pass
            HealAiUnit()
        else:
            logs.append(
                f'{user_units[index].name} is not high enough rank to heal!')
            for log in logs:
                try:
                    AddToGamelog(log)
                    AddToLogfile(log)
                except:
                    pass

    else:
        logs = []
        logs.append(f'{user_units[index].name} is already dead!')
        for log in logs:
            try:
                AddToGamelog(log)
                AddToLogfile(log)
            except:
                pass


# function to heal ai units
def HealAiUnit():
    # check which ai unit has rank > 1
    index = -1
    for i in range(0, 3):
        if aiUnits[i].rank > 1 and aiUnits[i].health_point > 0:
            index = i
    # if a unit has health greater than  1 then heal it
    if index > -1:
        # again calculate health using given formula
        selectedUnit = aiUnits[index]
        second_wind = 100*selectedUnit.rank*0.2
        if selectedUnit.health_point < 100:
            logs = []
            selectedUnit.health_point = selectedUnit.health_point + second_wind
            selectedUnit.rank = selectedUnit.rank - 1
            logs.append(
                f'{selectedUnit.name} healed , present health is {selectedUnit.health_point}!')
            ai_frame_components[index]["health_bar"]["value"] = selectedUnit.health_point
            for log in logs:
                try:
                    AddToGamelog(log)
                    AddToLogfile(log)
                except:
                    pass


# function to attack player units
def AttackCharacterUnit():
    # find the target unit
    target = user_units[0]
    index = 0
    for i in range(1, 3):
        if user_units[i].health_point > target.health_point:
            target = user_units[i]
            index = i
    # select a random attacker
    attacker_index = random.randint(0, 2)
    while aiUnits[attacker_index].health_point <= 0:
        attacker_index = (attacker_index + 1) % 3
    attacker = aiUnits[attacker_index]
    logs = []
    # again calculate damage using given formula
    damage = attacker.attack_point - \
        target.defense_point + random.randint(-5, 10)
    user_units[index].health_point -= damage
    attacker.experience_point += damage
    # append experience points
    def_exp = target.defense_point
    if damage > 10:
        def_exp = def_exp + def_exp*0.2
    if damage <= 0:
        def_exp = def_exp + def_exp*0.5
    target.experience_point += def_exp
    # append rank
    if (target.experience_point >= 100):
        target.experience_point = target.experience_point - 100
        target.rank = target.rank + 1
    if (attacker.experience_point >= 100):
        attacker.experience_point = attacker.experience_point - 100
        attacker.rank = attacker.rank + 1
    # display health
    character_frame_components[index]["health_bar"]["value"] = user_units[index].health_point
    logs.append(
        f'{attacker.name} attacked {target.name} for {attacker.attack_point} damage!')
    logs.append(f'{target.name} has {target.health_point} health left!')
    logs.append(
        f'{target.name} has {target.experience_point} experience points!')
    logs.append(f'{target.name} is rank {target.rank}!')
    logs.append(
        f'{attacker.name} has {attacker.experience_point} experience points!')
    logs.append(f'{attacker.name} is rank {attacker.rank}!')
    if target.health_point <= 0:
        logs.append(f'{target.name} has died!')
    for log in logs:
        try:
            AddToGamelog(log)
            AddToLogfile(log)
        except:
            pass
    CheckWinner()

# function to rewrite the log text file


def Overwritelogfile():
    with open("gamelog.txt", "w") as file:
        file.write("The Log of the game is as follows: \n")

# function to add logs in the txt file


def AddToLogfile(text):
    with open("gamelog.txt", "a") as file:
        file.write(text + "\n")

# function to check if there is a winner


def CheckWinner():
    isWinner = False
    Winner = ""
    # check if any of the player units are dead
    for i in range(0, 3):
        if user_units[i].health_point <= 0:
            isWinner = True
            Winner = "AI"
        else:
            isWinner = False
            Winner = ""
            break
    if isWinner:
        gamelog.insert(tk.END, f"{Winner} has won the game!")
        AddToLogfile(f"{Winner} has won the game!")
        ending_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        AddToLogfile(f"Game ended at {ending_time}")
        gamelog.see(tk.END)
        messagebox.showinfo("Game Over", f"{Winner} has won the game!")
        root.destroy()
        return
    # check if any of the ai units are dead
    for i in range(0, 3):
        if aiUnits[i].health_point <= 0:
            isWinner = True
            Winner = "Player"
        else:
            isWinner = False
            Winner = ""
            break
    if isWinner:
        gamelog.insert(tk.END, f"{Winner} has won the game!")
        AddToLogfile(f"{Winner} has won the game!")
        ending_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        AddToLogfile(f"Game ended at {ending_time}")
        gamelog.see(tk.END)
        messagebox.showinfo("Game Over", f"{Winner} has won the game!")
        root.destroy()

# function to display related information of user and ai units


def ShowInfo():
    logs = []
    logs.append(f'Player Units:')
    # display stats of the characters
    for i in range(0, 3):
        if user_units[i].health_point <= 0:
            logs.append(f'{user_units[i].name} is dead!')
            continue
        logs.append(
            f'{user_units[i].name} has {user_units[i].health_point} health points, {user_units[i].attack_point} attack points, {user_units[i].defense_point} defense points, {user_units[i].experience_point} experience points and is rank {user_units[i].rank}')
    logs.append(f'AI Units:')
    for i in range(0, 3):
        if aiUnits[i].health_point <= 0:
            logs.append(f'{aiUnits[i].name} is dead!')
            continue
        logs.append(
            f'{aiUnits[i].name} has {aiUnits[i].health_point} health points, {aiUnits[i].attack_point} attack points, {aiUnits[i].defense_point} defense points, {aiUnits[i].experience_point} experience points and is rank {aiUnits[i].rank}')
    for log in logs:
        AddToGamelog(log)
        AddToLogfile(log)


# function to create the user units
def UserCreationThroughGUi():

    # Ask the user for the name of the units and their type
    def getInputs():
        # get the name and types of the units
        name = name_entry.get()
        type = type_entry.get()
        name_1 = name_entry_1.get()
        # check cases
        if name == "":
            name = "Player 1"

        type_1 = type_entry_1.get()
        if name_1 == "":
            name_1 = "Player 2"

        name_2 = name_entry_2.get()
        type_2 = type_entry_2.get()
        if name_2 == "":
            name_2 = "Player 3"

        # checking types of units
        if type == "warrior" or type == "Warrior" or type == "WARRIOR" or type == "w" or type == "W":
            unit = Warrior()
            unit.name = name
        else:
            unit = Tanker()
            unit.name = name
        if type_1 == "warrior" or type_1 == "Warrior" or type_1 == "WARRIOR" or type_1 == "w" or type_1 == "W":
            unit_1 = Warrior()
            unit_1.name = name_1
        else:
            unit_1 = Tanker()
            unit_1.name = name_1
        if type_2 == "warrior" or type_2 == "Warrior" or type_2 == "WARRIOR" or type_2 == "w" or type_2 == "W":
            unit_2 = Warrior()
            unit_2.name = name_2
        else:
            unit_2 = Tanker()
            unit_2.name = name_2
        # add the units to the list
        user_units.append(unit)
        user_units.append(unit_1)
        user_units.append(unit_2)
        root1.destroy()

    # create the window and necessary labels and entries
    root1 = tk.Tk()
    root1.title("Create Units")
    name_label = tk.Label(root1, text="Name for Unit 1:",
                          font=("Arial", 12, "bold"))
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(root1)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # create type label and entry
    type_label = tk.Label(root1, text="Type for Unit 1:",
                          font=("Arial", 12, "bold"))
    type_label.grid(row=1, column=0, padx=10, pady=10)
    type_entry = tk.Entry(root1)
    type_entry.grid(row=1, column=1, padx=10, pady=10)

    name_label_1 = tk.Label(
        root1, text="Name for Unit 2:", font=("Arial", 12, "bold"))
    name_label_1.grid(row=2, column=0, padx=10, pady=10)
    name_entry_1 = tk.Entry(root1)
    name_entry_1.grid(row=2, column=1, padx=10, pady=10)

    # create type label and entry
    type_label_1 = tk.Label(
        root1, text="Type for Unit 2:", font=("Arial", 12, "bold"))
    type_label_1.grid(row=3, column=0, padx=10, pady=10)
    type_entry_1 = tk.Entry(root1)
    type_entry_1.grid(row=3, column=1, padx=10, pady=10)

    name_label_2 = tk.Label(
        root1, text="Name for Unit 3:", font=("Arial", 12, "bold"))
    name_label_2.grid(row=4, column=0, padx=10, pady=10)
    name_entry_2 = tk.Entry(root1)
    name_entry_2.grid(row=4, column=1, padx=10, pady=10)

    # create type label and entry
    type_label_2 = tk.Label(
        root1, text="Type for Unit 3:", font=("Arial", 12, "bold"))
    type_label_2.grid(row=5, column=0, padx=10, pady=10)
    type_entry_2 = tk.Entry(root1)
    type_entry_2.grid(row=5, column=1, padx=10, pady=10)

    # create ok button
    ok_button = tk.Button(root1, text="Create Units",
                          command=getInputs, font=("Arial", 12, "bold"))
    ok_button.grid(row=6, column=0, columnspan=2, pady=20)

    root1.mainloop()

##################################################################
# Main Loop COde


# Create user units
UserCreationThroughGUi()
# Create Ai unit
CreateAiUnit()
# Create Player unit
# Override log text file
Overwritelogfile()

# width and height of window
width = 800
game_width = 400
gamelog_width = 400
height = 600

# creating window
root = tk.Tk()
root.geometry(f"{1600}x{600}")
root.title("Turn Based Master")

# creating game frame which contains the game and gamelog frame which contains the gamelog
game_frame = tk.Frame(root, width=game_width, height=300)
gamelog_frame = tk.Frame(root, width=gamelog_width,
                         height=300, bd=1, relief="solid")
# displaying the frames
game_frame.grid(row=0, column=1, padx=50, pady=50)
gamelog_frame.grid(row=0, column=0, padx=50, pady=50)

# creating and displaying exit button
exit_button = tk.Button(root, text="Exit Game ",
                        command=root.destroy, bg="#33CAFF")
exit_button.config(font=('Ariel', 15))

# creating and displaying show info button
show_info_button = tk.Button(
    root, text="Show Info", bg="#33CAFF", command=ShowInfo)
show_info_button.config(font=('Ariel', 15))

show_info_button.grid(row=1, column=0, pady=10)

exit_button.grid(row=1, column=1, pady=10)
# creating and displaying the game log title
gamelog_titleframe = tk.Frame(gamelog_frame, width=20, height=20)
gamelog_titleframe.pack(side=tk.TOP)

gamelog_title = tk.Label(
    gamelog_titleframe, text="Game Log", font=('Ariel', 10))
gamelog_title.pack(side=tk.TOP, fill=tk.X)

# creating text frame for game log
gamelog_textframe = tk.Frame(gamelog_frame, width=gamelog_width, height=250)
gamelog_textframe.pack(side=tk.BOTTOM, fill=tk.X)

gamelog_textframe.config(width=400)


# creating scrollbar for game log
scrollbar = tk.Scrollbar(gamelog_textframe)


scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# appending information
gamelog = tk.Text(gamelog_textframe, yscrollcommand=scrollbar.set)
gamelog.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar.config(command=gamelog.yview)

game_label = tk.Label(game_frame, text="Game")
game_label.config(font=("Ariel", 44))

# Creating character frames
CreateCharacterFrame()
CreateAiFrame()
try:
    for i in range(0, 3):
        character_frame_components[i]["frame"].grid(row=i, column=0, padx=120)
        ai_frame_components[i]["frame"].grid(row=i, column=1)
except:
    print("Please create units first by restarting the game")
    sys.exit()

AddToGamelog("The game has started!")
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
AddToLogfile(f"The game has started at {timestamp}")

# calling the main loop so it runs over and over again
root.mainloop()
