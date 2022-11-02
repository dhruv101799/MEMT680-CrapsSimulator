import numpy as np

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
        self.diceA = 1 #Initialize dice to 1
        self.diceB = 1 #Initialize dice to 1
    def roll(self):
        self.diceA = np.random.randint(1, 7) #Generate random number between 1-6
        self.diceB = np.random.randint(1, 7) #Generate random number between 1-6

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
        self.bankroll = int(self.bankroll)

#BETS Class handles player betting and win/loss logic
class Bets(Player):
    def __init__(self):
        super().__init__()
        self.possibleBets = ["No Bet", "Pass Line", "Do Not Pass", "Odds Bet"] # Define possible bets
        self.activeBets = {"No Bet": 0, "Pass Line": 0, "Do Not Pass": 0, "Odds Bet": 0} #Initizalize active bets to 0
        self.betAmount = 0 #Initialize bet amount (default = 0)

    def check_funds(self, betAmount:int) -> int:
        # while not checkInt(betAmount): #Repeatedly ask for bet amount until valid integer input is given
        #     betAmount = input("Enter a valid integer bet amount: ")
        betAmount = int(betAmount)
        
        while True:
            if int(betAmount) > self.bankroll:
                betAmount = input(f"{self.name}, you have insufficient funds for a bet of ${betAmount}.\nYour bankroll is: ${self.bankroll}\nPlease enter a valid integer bet amount: ")
                
                while not checkInt(betAmount): #Repeatedly ask for bet amount until valid integer input is given
                    betAmount = input("Enter a valid integer bet amount: ")
            else:
                return int(betAmount)
        

    def pass_line_bet(self, betAmount):
        if self.point:
            self.betAmount = self.check_funds(betAmount) #Check if requested bet amount is possible with current funds
            print(f"A bet on the pass line of ${self.betAmount} was placed by {self.name}.")
            self.activeBets['pass line'] = self.betAmount
            self.bankroll = self.bankroll - self.betAmount
        else:
            print("The point has not been set and a pass line bet cannot be placed.")

    def do_not_pass_bet(self, betAmount):
        if not self.point:
            self.betAmount = self.check_funds(betAmount) #Check if requested bet amount is possible with current funds
            print(f"A bet on the do not pass line of ${self.betAmount} was placed by {self.name}.")
            self.activeBets['do not pass'] = self.betAmount
            self.bankroll = self.bankroll - self.betAmount
        else:
            print("The point has not been set and a pass line bet cannot be placed.")
    
    def betting_turn(self):
        bet_decision = input(f"{self.name}, would you like to place any bets (y/n)? ")
        valid_decisions = ["y", "yes", "n", "no"]
        valid_betTypes = ["a", "pass line", "b", "do not pass line"]
        while bet_decision.lower() not in valid_decisions: #Check decision
            #Valid decision was not chosen
            bet_decision = input(f"{self.name}, you did not enter a valid choice. Please select (y/n) to place a bet: ")

        #Process valid decision to place bet:
        if bet_decision.lower() == "y" or bet_decision.lower() == "yes": #Player would like to place a bet
            print("Where would you like to place a bet?\n(A) Pass Line\n(B)Do Not Pass Line")
            betType = input("Bet location (A/B): ").lower()
            while betType not in valid_betTypes: #Check bet
                betType = input("Please enter a valid bet location (A/B): ").lower() #Repeatedly ask for valid bet choice
                
            #Process chosen bet
            if betType == "a": # Pass line bet
                print(f"{self.name} placed a valid bet on the pass line")
                betLocation = "Pass Line"
                self.activeBets[betLocation] = self.ingestBet(betLocation) #Get bet amount
            else: # Do not pass line bet
                print(f"{self.name} placed a valid bet on the do not pass line")
                betLocation = "Do Not Pass"
                self.activeBets[betLocation] = self.ingestBet(betLocation) #Get bet amount
                

        else: #Player does not wish to place a bet at this time
            print(f"{self.name} does NOT place bet")

    def ingestBet(self, betLocation) -> int: 
        betAmount = input(f"{self.name}, please enter a valid bet amount for the {betLocation}: ")
        while betAmount == 0 or not checkInt(betAmount): #Repeatedly ask for bet amount until valid non-zero integer input is given
            betAmount = input(f"Enter a valid non-zero integer bet amount for {betLocation}: ")
        return int(betAmount)

player1 = Bets()
print(f"{player1.name} has a bankroll of ${player1.bankroll}.")
player1.betting_turn()

# player1.point = True
# player1.pass_line_bet(betAmount=input(f"{player1.name}, how much would you like to bet on the pass line?\nEnter a valid integer bet amount: "))
# player1.point = False
# player1.do_not_pass_bet(betAmount=input(f"{player1.name}, how much would you like to bet on the do not pass line?\nEnter a valid integer bet amount: "))