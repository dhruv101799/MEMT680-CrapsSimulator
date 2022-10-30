#DICE Class that holds current value of 2 dice
class Dice:
    def __init__(self):
        pass
    def roll(self):
        pass

#TABLE Class defines if point has been set
class Table(Dice):
    def __init__(self):
        super().__init__() #Enables reference to parent class without needing to explicitly call them
        self.point = False #Initialize set point to false

#PLAYER Class defines properties of player
class Player(Table):
    def __init__(self):
        super().__init__()
        self.name = input("Enter player name: ") #Request and save player name
        while True:
            try:
                self.bankroll = input("Enter your bankroll: ") #Get amount of money player has on table
                if not isinstance(self.bankroll, int):
                    raise ValueError
            except ValueError:
                print("Please enter a valid integer value for your bankroll (e.g., 100)")

def ErrorHandler(func):
    def checkInput(x):
        if not isinstance(x, int):
            raise Exception("Input must be a valid integer value...")
        userInput = func(x)
        return userInput
    return checkInput