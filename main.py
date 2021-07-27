from CurrentTokenBalance import *
#################################
##    Change this portion    ####
## Fill with wallet addresses ###
#################################
address_lst = []
#################################
##Comment###
balance = CurrentBalance(address_lst)
df_balance = balance.getCurrentBalances()
