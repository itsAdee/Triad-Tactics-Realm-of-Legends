import random
# there are two types of units: Warrior and Tanker
# each unit has a name, health point, experience point, rank, attack point, and defense point

# Class Unit is the parent class of Warrior and Tanker


class Unit:
    def __init__(self):
        # attributes
        self.name = ""
        self.health_point = 100
        self.experience_point = 0
        self.attack_point = 0
        self.defense_point = 0
        self.rank = 1
        self.type = ""
    # Attack Function

    def attack(self, enemy):
        # calculate damage
        damage = self.attack_point - \
            enemy.defense_point + random.randint(-5, 10)
        # check if damage is negative
        if damage < 0:
            damage = 0
        # return damage
        return damage

    # check if unit is alive or not
    def isAlive(self):
        return self.health_point > 0

    # function to decrease health point based on damage dealt
    def sustain_damage(self, damage):
        self.health_point -= damage
        if self.health_point < 0:
            self.health_point = 0

    # function to increase experience point based on damage dealt
    def get_attack_experience(self, damage):
        self.experience_point += abs(damage)
        self.experience_point = round(self.experience_point, 2)
        return self.experience_point

    # function to increase experience point based on damage received
    def get_defense_experience(self, damage):
        def_exp = abs(damage)
        # additional experience if damage is greater than 10
        if damage > 10:
            def_exp = def_exp + def_exp*0.2
        # additional experience if damage is less than or equal to 0
        if damage <= 0:
            def_exp = def_exp + def_exp*0.5
        # add experience to experience point
        self.experience_point += def_exp
        # round experience point to 2 decimal places
        self.experience_point = round(self.experience_point, 2)
        return self.experience_point

    # function to perform heal function
    def heal(self):
        # check if unit has rank greater than 1
        if self.rank > 1:
            # calculate second wind
            second_wind = 100*self.rank*0.1
            second_wind = round(second_wind, 2)
            # increase health point
            self.health_point += second_wind
            # check if health point is greater than 100
            if self.health_point > 100:
                self.health_point = 100
            # round health point to 2 decimal places
            self.health_point = round(self.health_point, 2)
            return second_wind
        else:
            return 0

    # function to promote unit based on experience point
    def promote(self):
        if self.experience_point >= 100:
            self.rank += 1
            self.experience_point -= 100

    # function to get rank
    def get_rank(self):
        return self.rank

    # function to show_info of unit
    def show_info(self):
        info = f"{self.name} has {self.health_point} health points, {self.experience_point} experience points, {self.rank} rank, {self.attack_point} attack points, and {self.defense_point} defense points."
        return info
    # function to get health point

    def get_health(self):
        return self.health_point

# Class Warrior is the child class of Unit


class Warrior(Unit):
    def __init__(self):
        super().__init__()
        # attributes
        self.attack_point = random.randint(5, 20)
        self.defense_point = random.randint(1, 10)

# Class Tanker is the child class of Unit


class Tanker(Unit):
    def __init__(self):
        super().__init__()
        # attributes
        self.attack_point = random.randint(1, 10)
        self.defense_point = random.randint(5, 15)
