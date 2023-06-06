from gamecomponents import *
from units import *
from logs import *
from datetime import datetime
import sys


# initialize the game
new_game = GameComponents()
# initialize the logs
gamelog = Gamelog('gamelog.txt')
gamelog.clear()
consolelog = Consolelog()
# create the units
new_game.CreatePlayerUnits()
new_game.CreateAiUnits()


def announce_Winner():
    # announce the winner
    winner = new_game.CheckWinner()
    if winner != "None":
        s = f"\n{winner} has won the game"
        write_to_logs(s)
        sys.exit()

# main function
# this function is called when the game starts


def ask_user_to_attack_or_heal_or_showinfo():
    # ask the user to attack or heal or show info
    option = input(
        "\nMenu:\n'a': Attack - 'h': Heal - 's': Player Info - 'e': Exit\nEnter Option: ")
    # if the user wants to attack
    if option in ['a', 'h']:
        if option == 'a':
            # ask the user to select the unit which will attack
            attackSelection()
        else:
            # ask the user to select the unit which will heal
            healSelection()
        # check if the game is over
        announce_Winner()
        # Ai's turn
        print("\nComp's Turn")
        # call the ai attack function
        if option == 'a':
            aiattackselection()
        else:
            aihealselection()
        print("Comp's Turn Completed\n")
        # check if the game is over
        announce_Winner()
        print("Moving to next turn")
    elif option == 's':
        # show the details of the units
        print("\nUnit Details:\n")
        ShowDetails()
    elif option == 'e':
        sys.exit()
    else:
        print("Invalid input.")
    ask_user_to_attack_or_heal_or_showinfo()


def write_to_logs(content):
    # write the content to the logs
    consolelog.clear()
    gamelog.write(content)
    consolelog.consolelog.append(content)
    consolelog.write()

# function to select the attacker


def attackSelection():
    # ask the user to select the unit which will attack
    option = input("Enter Attacker Unit Index: ")
    # if the user enters a valid input
    if option.isdigit():
        # convert the input to integer
        option = int(option)
        # if the input is in the range of the units
        if option in range(len(new_game.userUnits)):
            if not new_game.userUnits[option].isAlive():
                print("Unit is dead. Please select another unit.")
                return attackSelection()
            attacker = new_game.userUnits[option]
            enemySelectionforattack(attacker)
        # if the input is not in the range of the units
        else:
            print("Invalid input. Please enter a number between 0 and " +
                  str(len(new_game.userUnits) - 1))
            return attackSelection()
    else:
        print("Invalid input. Please enter a number.")
        return attackSelection()


# function to select the defender
def enemySelectionforattack(attacker):
    # ask the user to select the unit which will be attacked
    option = input(
        "Enter Enemy Unit Index: ")
    # if the user enters a valid input
    if option.isdigit():
        option = int(option)
        if option in range(len(new_game.AiUnits)):
            if not new_game.AiUnits[option].isAlive():
                print("Unit is dead. Please select another unit.")
                return enemySelectionforattack(attacker)
            # select the defender
            defender = new_game.AiUnits[option]
            # get the damage
            damage = attacker.attack(defender)
            # update experience
            attacker_exp = attacker.get_attack_experience(damage)
            defender.sustain_damage(damage)
            defender_exp = defender.get_defense_experience(damage)
            # promote the units
            attacker.promote()
            defender.promote()
            # get the health of the defender
            defender_health = defender.get_health()
            # write the logs

            write_to_logs(f"\n{attacker.name} attacked {defender.name}, {damage} damage.\n{defender.name}'s remaining health: {defender_health} points.\n{attacker.name} gained {attacker_exp} experience.\n{defender.name} gained {defender_exp} experience.")
        else:
            print("Invalid input. Please enter a number between 0 and " +
                  str(len(new_game.AiUnits) - 1))
            return enemySelectionforattack(attacker)
    else:
        print("Invalid input. Please enter a number.")
        return enemySelectionforattack(attacker)

# function thorugh which the Ai selects the attacker and deals damage


def aiattackselection():
    # find the target unit
    target = new_game.userUnits[0]
    index = 0
    # find the unit with the highest health
    for i in range(1, 3):
        if new_game.userUnits[i].health_point > target.health_point and new_game.userUnits[i].isAlive():
            target = new_game.userUnits[i]
            index = i
    # select a random attacker
    attacker_index = random.randint(0, 2)
    while new_game.AiUnits[attacker_index].health_point <= 0:
        attacker_index = (attacker_index + 1) % 3
    # get the attacker
    attacker = new_game.AiUnits[attacker_index]
    # deal damage
    damage = attacker.attack(target)
    target.sustain_damage(damage)
    # update experience
    attacker_exp = attacker.get_attack_experience(damage)
    defender_exp = target.get_defense_experience(damage)
    # promote the units
    attacker.promote()
    target.promote()
    defender_health = target.get_health()
    # write the logs
    write_to_logs(f"\n{attacker.name} attacked {target.name}, dealing {damage} damage.\n{target.name}'s remaining Health: {defender_health} points.\n{attacker.name} gained {attacker_exp} experience.\n{target.name} gained {defender_exp} experience.")


# function to select the unit which will heal
def healSelection():
    # ask the user to select the unit which will heal
    option = input(
        "Enter Index of Unit to heal: ")
    # if the user enters a valid input
    if option.isdigit():
        option = int(option)
        # if the input is in the range of the units
        if option in range(len(new_game.userUnits)):
            if not new_game.userUnits[option].isAlive():
                print("Unit is dead. Please select another unit.")
                return ask_user_to_attack_or_heal_or_showinfo()
            # select the unit which will heal
            unit_to_heal = new_game.userUnits[option]
            healed_points = unit_to_heal.heal()
            # check if the unit has enough rank to heal
            if healed_points == 0:
                write_to_logs(
                    f"{unit_to_heal.name} does not have enough level to heal.")
                return ask_user_to_attack_or_heal_or_showinfo()
            else:
                write_to_logs(
                    f"{unit_to_heal.name} healed {healed_points} points.")
        else:
            print("Invalid input. Please enter a number between 0 and " +
                  str(len(new_game.userUnits) - 1))
            return healSelection()
    else:
        print("Invalid input. Please enter a number.")
        return healSelection()


def aihealselection():
    # check which ai unit has rank > 1
    index = -1
    for i in range(0, 3):
        if new_game.AiUnits[i].rank > 1 and new_game.AiUnits[i].isAlive():
            index = i
    # if a unit has health greater than  1 then heal it
    index = int(index)
    if index > -1:
        # again calculate health using given formula
        selectedUnit = new_game.AiUnits[index]
        health_points = selectedUnit.heal()
        write_to_logs(
            f"{selectedUnit.name} healed {health_points} points.\nRemaining Health: {selectedUnit.health_point} points.")


# function to show the details of the units
def ShowDetails():
    print("Player Units")
    for i in range(0, len(new_game.userUnits)):
        print(
            f"{i}: Name: {new_game.userUnits[i].name}, health: {new_game.userUnits[i].health_point}, Rank: {new_game.userUnits[i].rank}, Experience: {new_game.userUnits[i].experience_point}, Defence: {new_game.userUnits[i].defense_point}, Attack: {new_game.userUnits[i].attack_point}")
    print("Comp Units")
    for i in range(0, len(new_game.AiUnits)):
        print(
            f"{i}: Name: {new_game.AiUnits[i].name}, health: {new_game.AiUnits[i].health_point}, Rank: {new_game.AiUnits[i].rank}, Experience: {new_game.AiUnits[i].experience_point}, Defence: {new_game.AiUnits[i].defense_point}, Attack: {new_game.AiUnits[i].attack_point}")


print(" --- Welcome to the game --- ")
print("\nOpening Stats:\n")
ShowDetails()
ask_user_to_attack_or_heal_or_showinfo()
