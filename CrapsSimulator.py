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
        self.diceA = 0 #Initialize dice to 0
        self.diceB = 0 #Initialize dice to 0
        self.roll_outcome = self.diceA + self.diceB # Initialize roll outcome
    def roll(self):
        self.diceA = np.random.randint(1, 7) #Generate random number between 1-6
        self.diceB = np.random.randint(1, 7) #Generate random number between 1-6
        return self.diceA + self.diceB

#TABLE Class defines if point has been set
class Table(Dice):
    def __init__(self):
        super().__init__() #Enables reference to parent class without needing to explicitly call them
        self.comeout = True #Initialize first roll as comeout roll
        self.point = False #Initialize set point to false
        self.point_value = 0 # Initizalize point value to 0

#PLAYER Class defines properties of player
class Player(Table):
    def __init__(self):
        super().__init__()
        self.name = input("Enter player name: ") #Request and save player name
        self.bankroll = input("Enter your bankroll: ") #Get amount of money player has on table
        while not checkInt(self.bankroll): #Repeatedly ask for bankroll until valid input is given
            self.bankroll = input("Enter your bankroll: ")
        self.bankroll = int(self.bankroll)
        self.isShooter = False # Initialize player to not be shooter until non-zero bets are placed

#BETS Class handles player betting and win/loss logic
class Bets(Player):
    def __init__(self):
        super().__init__()
        self.possibleBets = ["Pass Line", "Do Not Pass", "Odds Bet"] # Define possible bets
        self.activeBets = {"Pass Line": 0, "Do Not Pass": 0, "Odds Bet": 0} #Initizalize active bets to 0
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
        

    def pass_line_bet(self):
        if not self.point:
            betLocation = "Pass Line"
            self.activeBets[betLocation] = self.activeBets[betLocation] + self.ingestBet(betLocation) #Get bet amount
            self.bankroll = self.bankroll - self.activeBets['Pass Line']
            print(f"A bet on the pass line of ${self.activeBets['Pass Line']} was placed by {self.name}.")
            self.printActiveBets()
            self.betting_turn()
        else:
            print("The point has not been set and a pass line bet cannot be placed.")

    def do_not_pass_bet(self):
        if not self.point:
            betLocation = "Do Not Pass"
            self.activeBets[betLocation] = self.activeBets[betLocation] + self.ingestBet(betLocation) #Get bet amount
            self.bankroll = self.bankroll - self.activeBets['Do Not Pass']
            print(f"A bet on the do not pass line of ${self.activeBets['Do Not Pass']} was placed by {self.name}.")
            self.printActiveBets()
            self.betting_turn()
        else:
            print("The point has been set and a do not pass line bet cannot be placed.")
    
    def betting_turn(self):
        bet_decision = input(f"{self.name}, would you like to place any bets (y/n)? ")
        valid_decisions = ["y", "yes", "n", "no"]
        valid_betTypes = ["a", "pass line", "b", "do not pass line", "c", "odds bet"]
        while bet_decision.lower() not in valid_decisions: #Check decision
            #Valid decision was not chosen
            bet_decision = input(f"{self.name}, you did not enter a valid choice. Please select (y/n) to place a bet: ")

        #Process valid decision to place bet:
        if bet_decision.lower() == "y" or bet_decision.lower() == "yes": #Player would like to place a bet
            print("Where would you like to place a bet?\n(A) Pass Line\n(B) Do Not Pass Line\n(C) Odds Bet")
            betType = input("Bet location (A/B/C): ").lower()
            while betType not in valid_betTypes: #Check bet
                betType = input("Please enter a valid bet location (A/B/C): ").lower() #Repeatedly ask for valid bet choice
                
            #Process chosen bet
            if betType == "a": # Pass line bet
                print("\nPASS LINE BET")
                self.pass_line_bet()
                self.Shooter()
            elif betType == "b": # Do not pass line bet
                print("\nDO NOT PASS BET")
                self.do_not_pass_bet()
                self.Shooter()
            else: # Odds bet
                print("\nODDS BET")
                self.Odds()
                self.Shooter()

        else: #Player does not wish to place a bet at this time
            print(f"\n{self.name} chose not to place a bet this round")
            self.Shooter()

    #Get bet amount from user, verify non-zero integer input, and return
    def ingestBet(self, betLocation) -> int:
        betAmount = input(f"{self.name}, please enter a valid bet amount for the {betLocation}: ")
        while betAmount == 0 or not checkInt(betAmount): #Repeatedly ask for bet amount until valid non-zero integer input is given
            betAmount = input(f"Enter a valid non-zero integer bet amount for {betLocation}: ")
        
        betAmount = self.check_funds(betAmount) #Check if requested bet amount is possible with current funds

        return int(betAmount)

    #Method to print active bets
    def printActiveBets(self): 
        #TODO: Print out active bets
        print("\n********ACTIVE BETS********\n")
        print("Bet Type\tBet Amount\n")
        for key,value in self.activeBets.items():
            print(f"{key}\t${value}")
        if self.point:
            print(f"\nThe point has been set to: {self.point_value}\n")
        print("\n***************************\n")

    #Method to process bet wins/losses
    def processBets(self):
        #TODO: After bets are placed and die are rolled, process bets (win/loss)
        #TODO: Print out bets won
        #TODO: Print out bets lost
        #TODO: Print bankroll at end of round after wins/losses
        
        if not self.point: # Comeout roll
            print(f"You rolled a: {self.roll_outcome}")
            set_point = [4, 5, 6, 8, 9, 10]
            pass_win = [7, 11]
            do_not_pass_win = [2, 3, 12]

            if self.roll_outcome in set_point:
                self.point = True # Set the point
                self.point_value = self.roll_outcome
                print(f"The point has been set to be: {self.point_value}\n")
                self.Shooter()

            elif self.roll_outcome in pass_win: # User wins pass line bet
                self.point = False # Point is not on table
                self.Bet_winner(betType="Pass Line")

            elif self.roll_outcome in do_not_pass_win: # User wins do not pass line bet on comeout roll
                self.Bet_winner(betType="Do Not Pass")

            else: # User loses pass line bet
                self.point = False # Point is not on table
                self.Bet_loser()

        else: # No longer a comeout roll because point has been set
            #Game changes to continuously roll until player "sevens out" or rolls point value
            print(f"You rolled a: {self.roll_outcome}")
            
            if self.roll_outcome == 7: # Player loses bet by "sevening out"
                self.point = False # Remove point from table
                self.point_value = 0 # Reset point value to 0
                self.Bet_loser() # Process lost bets
            elif self.roll_outcome == self.point_value:
                #Player wins by hitting point marker
                self.point = False # Remove point from table
                self.point_value = 0 # Reset point value to 0
                self.Bet_winner(betType="Pass Line") # Process winning bets
            else:
                print("\nYou missed the point, roll again!\n")
                self.Shooter()
                

    #Check if bets are active, roll die, evaluate payouts
    def Shooter(self):
        #TODO: Check if there are any active non-zero bets
        #TODO: If bets are active, roll die
        #TODO: Evaluate payouts for active bets after roll outcome
        self.isShooter = False

        for bet, amount in self.activeBets.items():
            if amount != 0: # Check if there are non-zero bets
                self.isShooter = True # Bet has been placed and shooter can roll die
                self.printActiveBets() # Show bets that are active before rolling die
                
                # Ask user if they are ready to roll die:
                roll_decision = input(f"{self.name}, ready to roll the die (y/n)? ")
                valid_decisions = ["y", "yes", "n", "no"]
                while roll_decision.lower() not in valid_decisions: #Check decision
                    #Valid decision was not chosen
                    roll_decision = input(f"{self.name}, you did not enter a valid choice. Please select (y/n) to roll the die: ")

                if roll_decision.lower() == "n":
                    print(f"\n{self.name} chose not to roll the die yet.")
                    self.betting_turn()
                else:
                    print("ROLLING DIE...")
                    self.roll_outcome = self.roll() # Generate random values for rolled die
                    self.processBets() # Process wins/losses
                    break
        
        if not self.isShooter: # No bets are active and shooter cannot roll die
            self.printActiveBets() # Show the user that there are no active bets
            print("There are no active bets. Please place a bet to roll die.")
            self.betting_turn() # Get player bets

    #Process losing bets
    def Bet_loser(self):
        #TODO: If bet is lost, print out bet location and amount lost
        #TODO: Call 'bets_lost()' method
        print("\nYou lost...")
        print(f"The roll was a {self.roll_outcome}")
        if self.point:
            print(f"The point was set to {self.point_value}")
        print("Here were the bets that you lost: ")
        self.printActiveBets()

        for bets in self.activeBets.keys():
            self.activeBets[bets] = 0 # Reset bet amounts to 0
        
        print(f"{self.name}, your remaining bankroll is ${self.bankroll}")
        self.printActiveBets()
        self.betting_turn()

    #Process winning bets
    def Bet_winner(self, betType):
        #TODO: Determine bet type and calculate winnings for wager
        #TODO: Adjust bankroll with new winnings using 'Payout()' method
        #TODO: Remove odds bets from active status and return to bankroll
        #TODO: Print winning data
        print(f"You won on {betType} with a bet of {self.activeBets[betType]}")

        self.Payout() # Evaluate winnings
        self.activeBets["Odds Bet"] = 0 # Set odds bet to 0 after payout has been made
        self.point = False # Remove point from table
        self.point_value = 0 # Initialize point value to 0 for next round

        self.printActiveBets() # Print active bets
        print(f"Your current bankroll is now: ${self.bankroll}")

        self.Shooter()
        pass

    #Process Odds bets
    def Odds(self):
        #TODO: Check if odds bet can be made (pass line bet must be active)
        #TODO: Determine maximum bet that can be placed 
        #TODO: Print maximum bet value and current bankroll for player
        #TODO: Place Odds bet using 'ingestBet()' method
        #TODO: Adjust bankroll after Odds bet is placed
        if self.point and self.activeBets["Pass Line"] != 0:
            print("Odds bet is being placed...")
        else:
            if self.activeBets["Pass Line"] == 0:
                print("A pass line bet has not been placed, so an odds bet cannot be made.")
            else:
                print("The point has not been set, so an odds bet cannot be placed.")

    #Process payouts
    def Payout(self):
        #TODO: Reconcile all bets based on outcomes
        #TODO: Check if there are active bets
        #TODO: If not active bets, prompt user to either make a bet or walk away with current bankroll
        #TODO: If bets are active, prompt user to roll dice again
        print("Processing payouts")
        pass


player1 = Bets()
print(f"{player1.name} has a bankroll of ${player1.bankroll}.")
player1.betting_turn()
print("\nThanks for playing!")

# player1.point = True
# player1.pass_line_bet(betAmount=input(f"{player1.name}, how much would you like to bet on the pass line?\nEnter a valid integer bet amount: "))
# player1.point = False
# player1.do_not_pass_bet(betAmount=input(f"{player1.name}, how much would you like to bet on the do not pass line?\nEnter a valid integer bet amount: "))