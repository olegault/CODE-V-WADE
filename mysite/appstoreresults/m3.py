import privpol

#file invoked when user clicks SUBMIT (after inputting the app store and/or priv pol urls)
#1. webscrape from api autocalled
#2. copy-paste URL from app store, which gets fed into NLP
#3. email PING gets sent to CVW email with info abt the app to prompt packet testing.

#EACH of 1,2 will output a binary array which each corresponds to questions (see metrics.txt) we use to decide score
#the qs for 3 will have a default of "0" until the packet testing is complete—@Miles can update site w new numbers


#a later workflow is a form to automatically update those numbers for miles, and a "not complete" tag for apps that dont have testing done yet

#last thing is to take a calculation of the total score (we can just do a basic "add all the value and multiply the sum by a nubmer for rn")
#then display


val = 0 #default for score




