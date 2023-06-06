# Define the Warrior and Tanker classes as before
import random


class Unit:
    def __init__(self):
        self.name = ""
        self.health_point = 100
        self.experience_point = 0
        self.rank = 1


class Warrior(Unit):
    def __init__(self):
        super().__init__()
        self.attack_point = random.randint(40, 80)
        self.defense_point = random.randint(1, 10)


class Tanker(Unit):
    def __init__(self):
        super().__init__()
        self.attack_point = random.randint(41, 80)
        self.defense_point = random.randint(5, 15)
