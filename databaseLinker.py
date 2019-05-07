#Unfinished Linker for Fingerprint User to Database
#Andre Britton and Darren Johnson
from db_orch import add_user

def fingerprintUserTransfer(string):
    #This function will be called everytime a valid user's finger is scanned
    #Example string="Valid Entry: Andre Britton Finger Found"
    wordList = string.split(" ")
    username = wordList[2] + " " + wordList[3]
    # add functionality here
    password = "example"
    email = "example@gmail.com"
    authenticated = "example"
    phonenumber = "13181110000"

    add_user(email, password, authenticated, username, phonenumber)
