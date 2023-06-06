from datetime import datetime


# This file contains the classes for the logs of the game.
class Gamelog:
    def __init__(self, filename):
        # filename is the name of the file where the gamelog will be stored
        self.filename = filename
        # gamelog is the list of the lines of the gamelog
        self.gamelog = []
        self.clear()

    # function to read the gamelog from the file
    def read(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.gamelog.append(line)

    # function to write the gamelog to the file
    def write(self, content):
        with open(self.filename, 'a') as f:
            current_time = datetime.now().strftime("%H:%M:%S")
            f.write(f"\n - {current_time} - {content}")
            for line in self.gamelog:
                f.write(line)

    # function to clear the gamelog
    def clear(self):
        with open(self.filename, 'w') as f:
            f.write('The log of the game is as follows:\n')

    # function to clear the gamelog list
    def cleargamelog(self):
        self.gamelog = []


# This class is used to store the console log
class Consolelog:
    def __init__(self):
        # consolelog is the list of the lines of the consolelog
        self.consolelog = []

    # function to add a line to the consolelog
    def write(self):
        for line in self.consolelog:
            print(line)

    # function to clear the consolelog list

    def clear(self):
        self.consolelog = []
