# def ErrorHandler(func):
#     def Inner_Function(*args, **kwargs):
#         try:
#             func(*args, **kwargs)
#             return True
#         except:
#             print(f"{func.__name__} was provided with wrong data types. Enter numeric values.")
#             return False
#     return Inner_Function

# @ErrorHandler
# def checkInt(x):
#     return int(x)
    
# x = input("Enter integer value: ")
# while not checkInt(x):
#     x = input("Enter integer value: ")

# print(x)
    
activeBets = {"Pass Line": 0, "Do Not Pass": 0, "Odds Bet": 0} #Initizalize active bets to 0
for bet, amount in activeBets.items():
    print(f"Bet: {bet}, Amount: ${amount}")