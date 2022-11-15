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
    def resetTable(self):
        self.point = False # Remove point from table
        self.point_value = 0 # Initialize point value to 0 for next round
        self.oddsPlaced = False # Rest odds bet tracker to False

#PLAYER Class defines properties of player
class Player(Table):
    def __init__(self):
        super().__init__()
        self.name = input("Enter player name: ") #Request and save player name
        self.bankroll = input("Enter your bankroll: ") #Get amount of money player has on table
        while not checkInt(self.bankroll) or int(self.bankroll) <= 0: #Repeatedly ask for bankroll until valid input is given
            self.bankroll = input("Enter a non-zero integer for your bankroll: ")
        self.bankroll = int(self.bankroll)
        self.startBankroll = int(self.bankroll) # Starting bankroll to compare win/loss at cash out
        self.isShooter = False # Initialize player to not be shooter until non-zero bets are placed

#BETS Class handles player betting and win/loss logic
class Bets(Player):
    def __init__(self):
        super().__init__()
        self.possibleBets = ["Pass Line", "Do Not Pass", "Odds Bet"] # Define possible bets
        self.activeBets = {"Pass Line": 0, "Do Not Pass": 0, "Odds Bet": 0} #Initizalize active bets to 0
        self.oddsPlaced = False # Track if odds bet was placed

    def check_funds(self, betAmount:int) -> int:
        betAmount = int(betAmount)
        
        while True:
            if int(betAmount) > self.bankroll: # Determine if satisfactory funds are available
                # Request valid fund amount based on bankroll
                betAmount = input(f"{self.name}, you have insufficient funds for a bet of ${betAmount}.\nYour bankroll is: ${self.bankroll}\nPlease enter a valid integer bet amount: ")
                
                while not checkInt(betAmount): #Repeatedly ask for bet amount until valid integer input is given
                    betAmount = input("Enter a valid integer bet amount: ")
            else:
                return int(betAmount) # Return verified bet amount
        

    def pass_line_bet(self):
        if not self.point: # If the point is not established
            betLocation = "Pass Line"
            betAmount = self.ingestBet(betLocation) #Get bet amount
            self.activeBets[betLocation] = self.activeBets[betLocation] + betAmount # Adjust bet category total
            self.bankroll = self.bankroll - betAmount # Adjust bankroll
            print(f"A bet on the {betLocation} of ${betAmount} was placed by {self.name}.")
            self.printActiveBets() # Output current bets
            self.betting_turn() # Ask user if they want to place more bets
        else: # Point has been established
            print("The point has been set and a pass line bet cannot be placed.")

    def do_not_pass_bet(self):
        if not self.point: # If the point is not established
            betLocation = "Do Not Pass"
            betAmount = self.ingestBet(betLocation) #Get bet amount
            self.activeBets[betLocation] = self.activeBets[betLocation] + betAmount # Adjust bet category total
            self.bankroll = self.bankroll - betAmount # Adjust bankroll
            print(f"A bet on the do not pass line of ${betAmount} was placed by {self.name}.")
            self.printActiveBets() # Output current bets
            self.betting_turn() # Ask user if the ywant to place more bets
        else: # Point has been established
            print("The point has been set and a do not pass line bet cannot be placed.")
    
    # Method to handle betting
    def betting_turn(self):
        # Process user input
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
                self.pass_line_bet() # Create pass line bet
                self.Shooter() # Call shooter method to roll die
            elif betType == "b": # Do not pass line bet
                print("\nDO NOT PASS BET")
                self.do_not_pass_bet() # Create do not pass bet
                self.Shooter() # Call shooter method to roll die
            else: # Odds bet
                print("\nODDS BET")
                self.Odds() # Create odds bet
                self.Shooter() # Call shooter method to roll die

        else: #Player does not wish to place a bet at this time
            print(f"\n{self.name} chose not to place a bet this round")
            self.Shooter() # Call shooter methdo to roll die

    #Get bet amount from user, verify non-zero integer input, and return
    def ingestBet(self, betLocation) -> int:
        if betLocation == "Odds Bet": #Maximum bet amount is restricted by bankroll and point value
            betAmount = input(f"{self.name}, please enter a valid bet amount for the {betLocation} \n(MAX ODDS BET = {self.maxOddsBet}): ")
            while not checkInt(betAmount) or int(betAmount) <= 0 or int(betAmount) > self.maxOddsBet: #Repeatedly ask for bet amount until valid non-zero integer input is given
                betAmount = input(f"Enter a valid non-zero integer bet below the max limit for {betLocation}: ")
            
            betAmount = self.check_funds(betAmount) #Check if requested bet amount is possible with current funds
            
            return int(betAmount)

        else: #Standard pass/do not pass bet is being placed
            betAmount = input(f"{self.name}, please enter a valid bet amount for the {betLocation}: ")
            while not checkInt(betAmount) or int(betAmount) <= 0: #Repeatedly ask for bet amount until valid non-zero integer input is given
                betAmount = input(f"Enter a valid non-zero integer bet amount for {betLocation}: ")
            
            betAmount = self.check_funds(betAmount) #Check if requested bet amount is possible with current funds

            return int(betAmount)

    #Method to print active bets
    def printActiveBets(self): 
        print("\n********ACTIVE BETS********\n")
        print("Bet Type\tBet Amount\n")
        for key,value in self.activeBets.items():
            print(f"{key}\t${value}")
        if self.point:
            print(f"\nThe point has been set to: {self.point_value}\n")
        print(f"\nCurrent bankroll: ${self.bankroll}")
        print("\n***************************\n")

    #Method to process bet wins/losses
    def processBets(self):
        
        if not self.point: # Comeout roll
            print(f"You rolled a: {self.roll_outcome}")
            
            # Comeout roll classifications:
            set_point = [4, 5, 6, 8, 9, 10]
            pass_win = [7, 11]
            do_not_pass_win = [2, 3, 12]

            if self.roll_outcome in set_point:
                self.point = True # Set the point
                self.point_value = self.roll_outcome
                print(f"The point has been set to be: {self.point_value}\n")
                self.Shooter()

            elif self.roll_outcome in pass_win and self.activeBets["Pass Line"] != 0: # User wins pass line bet on comeout roll
                self.activeBets["Do Not Pass"] = 0 # Do not pass loses on natural comeout roll
                self.point = False # Point is not on table
                self.Bet_winner(betType="Pass Line") # Process win for pass line bet

            elif self.roll_outcome in do_not_pass_win and self.activeBets["Do Not Pass"] != 0: # User wins do not pass line bet on comeout roll
                self.activeBets["Pass Line"] = 0 # Pass line loses on do not pass win during comeout roll
                self.point = False # Point is not on table
                self.Bet_winner(betType="Do Not Pass") # Process win for do not pass bet

            else: # User loses pass line bet
                self.point = False # Point is not on table
                self.Bet_loser()

        else: # No longer a comeout roll because point has been set
            #Game changes to continuously roll until player "sevens out" or rolls point value
            print(f"You rolled a: {self.roll_outcome}")
            
            if self.roll_outcome == 7: # Player loses bet by "sevening out"
                self.Bet_winner("Do Not Pass") # Do not pass line wins during seven-out
                self.point = False # Remove point from table
                self.point_value = 0 # Reset point value to 0
                self.oddsPlaced = False # Rest odds bet tracker
                self.Bet_loser() # Process lost bets
            elif self.roll_outcome == self.point_value:
                #Player wins by hitting point marker
                self.Bet_winner(betType="Pass Line") # Process winning bets
                self.point = False # Remove point from table
                self.point_value = 0 # Reset point value to 0
            else:
                print("\nYou missed the point, roll again!\n")
                self.Shooter() # Roll die again
                

    #Check if bets are active, roll die, evaluate payouts
    def Shooter(self):
        self.isShooter = False # Determine if player is shooter (initialize to false)

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
            self.nextRound() # Ask user if they want to place another bet or cash out

    #Process losing bets
    def Bet_loser(self):
        print("\nYou lost...")
        print(f"The roll was a {self.roll_outcome}") # Output roll that lost bet(s)
        if self.point: # If point was set
            print(f"The point was set to {self.point_value}")
        print("Here were the bets that you lost: ") # Output losing bets
        self.printActiveBets()

        for bets in self.activeBets.keys():
            self.activeBets[bets] = 0 # Reset bet amounts to 0 after loss
        
        print(f"{self.name}, your remaining bankroll is ${self.bankroll}") # Output remaining bankroll after loss
        self.betting_turn() # Ask user to place new bets

    #Process winning bets
    def Bet_winner(self, betType):
        print(f"You won on {betType} with a bet of ${self.activeBets[betType]}") # Output winning bet

        self.Payout(betType) # Evaluate winnings            

        self.printActiveBets() # Print active bets

        self.betting_turn() # Ask player to place new bets for next round
        pass

    #Process Odds bets
    def Odds(self):
        # Payout structure for odds bet
        oddsBetMultiples = {3:[4, 10], 
                            4:[5, 9],
                            5:[6, 8]}

        if self.point and self.activeBets["Pass Line"] != 0: # Odds bet can be placed
            for multiple, point_val in oddsBetMultiples.items():
                if self.point_value in point_val:
                    odds_multiple = multiple # Define odds bet multiple based on point value
                    self.maxOddsBet = self.activeBets["Pass Line"] * odds_multiple # Define maximum odds bet amount

                    print(f"The point is set to: {self.point_value}")
                    print(f"Maximum odds bet that can be placed is: ${self.maxOddsBet}")
                    break

            # Place odds bet using defined values
            betLocation = "Odds Bet"
            betAmount = self.ingestBet(betLocation) #Get bet amount
            self.activeBets[betLocation] = self.activeBets[betLocation] + betAmount # Adjust bet category total
            self.bankroll = self.bankroll - betAmount # Adjust bankroll
            print(f"An odds bet of ${betAmount} was placed by {self.name}.")
            self.oddsPlaced = True # Set odds bet tracker to True
            self.printActiveBets() # Output active bets
            self.betting_turn() # Ask player if they wish to place more bets
                    
        else: # Odds bet cannot be placed
            if self.activeBets["Pass Line"] == 0:
                print("A pass line bet has not been placed, so an odds bet cannot be made.")
            else:
                print("The point has not been set, so an odds bet cannot be placed.")

    #Process payouts
    def Payout(self, betType):        
        winnings = 0 # Initialize winnings to 0

        oddsPayout = {4 : 2,
                      10 : 2,
                      5 : 3/2,
                      9 : 3/2,
                      6 : 6/5,
                      8 : 6/5} # Point value : payout odds

        print("PROCESSING PAYOUTS...")

        betAmount = self.activeBets[betType]
        
        if not self.oddsPlaced: #Standard betting without odds bet
            # Pass line and do not pass line bets (w/o odds)
            winnings += betAmount # winnings
            self.resetTable() # Reset table by removing point
        
        elif betType == "Pass Line" and self.oddsPlaced: # Pass line win with odds
            winnings += betAmount*2 + self.activeBets["Odds Bet"] * oddsPayout[self.point_value] # Pass winnings + odds winnings
            for bet in self.activeBets.keys():
                self.activeBets[bet] = 0 # Set initial bets to 0 after odds bet wins
            self.resetTable() # Reset table by removing point
        
        elif betType == "Do Not Pass": # Do not pass line win when odds are placed
            winnings += betAmount # winnings
            # For do not pass line win, pass line and odds bet lose
            self.activeBets["Pass Line"] = 0
            self.activeBets["Odds Bet"] = 0
            self.resetTable() # Reset table by removing point

        else:
            print("PAYOUT CANNOT BE PROCESSED...")

        winnings = np.floor(winnings) # Round payout value down
        self.bankroll += int(winnings) # Adjust bankroll with winnings

        for bet, amount in self.activeBets.items():
            if amount !=0:
                self.isShooter = True
        
        self.nextRound() # Ask user if they want to cash out or place another bet
       
    
    # Prompt user with choice to cash out or continue
    def nextRound(self):
        valid_decisions = ["p", "place bet", "c", "cash out"]

        if not self.isShooter: # No bets are active
            roundDecision = input(f"{self.name}, you have no active bets. \nWould you like to place a new bet (p) or cash out (c): ")
        
            while roundDecision.lower() not in valid_decisions: #Check decision
                #Valid decision was not chosen
                roundDecision = input(f"{self.name}, you did not enter a valid choice. \nWould you like to place a new bet (p) or cash out (c): ")

            #Process valid decision to place bet:
            if roundDecision.lower() == "p" or roundDecision.lower() == "place bet": #Player would like to place a bet
                self.betting_turn()
            else: # Cash out
                gameWinnings = self.bankroll - self.startBankroll # Compute winnings
                if gameWinnings >= 0:
                    print(f"\n{self.name}, your total winnings were ${gameWinnings}!\n")
                else:
                    print(f"\n{self.name}, your total winnings were -${gameWinnings*-1}!\n")
                print("Thanks for playing!\n")
                exit()
        else:
            self.Shooter() # Bets are active... roll the dice



player1 = Bets() # Create new instance of betting player
print(f"{player1.name} has a bankroll of ${player1.bankroll}.") # Request player bankroll
player1.betting_turn() # Ask player to begin betting
print("\nThanks for playing!") # Exit message