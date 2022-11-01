#Error handler decorator to validate input
def ErrorHandler(func):
    def Inner_Function(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except:
            print("A valid integer input was not provided. Please try again.")
            return False
    return Inner_Function

#Check if input is integer
@ErrorHandler
def checkInt(x):
    return int(x)

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
        self.bankroll = input("Enter your bankroll: ") #Get amount of money player has on table
        while not checkInt(self.bankroll): #Repeatedly ask for bankroll until valid input is given
            self.bankroll = input("Enter your bankroll: ") 

#BETS Class handles player betting and win/loss logic
class Bets(Player):
    def __init__(self):
        super().__init__()
        self.possibleBets = {"no_bet": 0, "pass_line": 0, "do_not_pass": 0, "odds_bet": 0}
        self.currentBet = possibleBets["no_bet"]
        

    def insufficient_funds(self):
        pass


#Test player class
player1 = Player()
print(f"{player1.name} has a bankroll of ${player1.bankroll}.")