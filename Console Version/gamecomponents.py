from units import *

# Class GameComponents will contain all the game components


class GameComponents:
    def __init__(self):
        # attributes
        self.turns = 0
        self.userUnits = []
        self.AiUnits = []

    # function to create player units
    def CreatePlayerUnits(self):
        print("Create Player Units:")
        for i in range(3):
            print(f"Unit {i + 1}:")
            # input name and type of unit
            name = input("Enter Name for the unit:")

            if name == "":
                print(
                    f"No name entered. By default, the unit will be named 'User Unit {i + 1}'.")
                name = f"User Unit {i + 1}"
            unit_type = input("Enter 'w' for Warrior or 't' for Tanker: ")
            # create unit based on input
            if unit_type == 'w':
                unit = Warrior()
                unit.name = name
                unit.type = 'warrior'
                self.userUnits.append(unit)
            elif unit_type == 't':
                unit = Tanker()
                unit.name = name
                unit.type = 'tanker'
                self.userUnits.append(unit)
            else:
                # if invalid input, create a warrior by default
                print("Invalid input. Please enter 'w' or 't'.")
                print("By default, the unit will be a Warrior.")
                unit = Warrior()
                unit.type = 'warrior'
                unit.name = name
                self.userUnits.append(unit)

        return True

    def CreateAiUnits(self):
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
                unit.type = 'warrior'
                self.AiUnits.append(unit)
            elif unit_type == 't':
                unit = Tanker()
                unit.name = name
                unit.type = 'tanker'
                self.AiUnits.append(unit)

    def CreatePseudoUnits(self):
        random_numbers = []
        for i in range(3):
            # randomly choose a type of unit
            unit_type = random.choice(['w', 't'])
            random_number = random.randint(1, 100)
            # make sure the random number is not repeated
            while random_number in random_numbers:
                random_number = random_number + 1
            # assign the random number to the unit
            name = "User:" + str(random_number)
            # add unit to the list
            if unit_type == 'w':
                unit = Warrior()
                unit.name = name
                unit.type = 'warrior'
                self.userUnits.append(unit)
            elif unit_type == 't':
                unit = Tanker()
                unit.name = name
                unit.type = 'tanker'
                self.userUnits.append(unit)

    # function to check if there is a winnner and game has ended or not

    def CheckWinner(self):
        # check if there is a winner
        isWinner = True
        Winner = ""
        # check if all user units are dead
        for unit in self.userUnits:
            if unit.isAlive():

                isWinner = False
        if isWinner:
            Winner = "Comp"
            return Winner
        isWinner = True
        # check if all Ai units are dead
        for unit in self.AiUnits:
            if unit.isAlive():

                isWinner = False
        if isWinner:
            Winner = "User"
            return Winner
        return "None"
