import sys
import urllib.request
import sqlite3 as sqLite
import schedule
import time
import os.path
from bs4 import BeautifulSoup
from twilio.rest import Client


# define global variables
URL = "https://www.awesomeminer.com/download/setup/releaseinfo.txt"
currentVersion = ""
userPhone = ""
minerPhone = ""
accountSID = ""
authToken = ""


# checks to see if there is an update for Awesome Miner
def check_for_updates():
    print("Checking for updates at: {}".format(time.localtime()))  # prints the current time when checking begins
    get_current_version()  # gets the current version of Awesome Miner

    # opens connection to database
    con = sqLite.connect('Awesome-Miner-DB.db')
    c = con.cursor()
    print("Connecting to database.")

    #gets the version in the database to compare with the current version
    dbVersionUgly = str(c.execute("SELECT version FROM INFO").fetchall())  # returns: ([' version number '])
    dbVersion = dbVersionUgly.split("\'")  # splits string by '
    dbVersion = dbVersion[1]  # uses the version number

    if dbVersion == currentVersion:  # database and current version are the same
        print("Current version already installed. Checking for updates again at 0700 tomorrow.")
        con.close()
    else:  # database version and current version are not the same
        print("Versions are not the same: " + dbVersion + " " + currentVersion)  # prints message to user
        c.execute("UPDATE INFO SET version = ? WHERE userPhone = ?",  # sets the new version in the database
                  (currentVersion, userPhone))
        con.commit()  # commits the version to the database

        # sends message to the user's phone from the Twilio number
        client = Client(accountSID, authToken)
        client.messages.create(to="+" + userPhone, from_="+" + minerPhone, body="New Awesome Miner Update Available! "
                               "Exiting Awesome Miner notification program. Please restart the program after "
                                "Awesome Miner has been updated.")
        print("Sending SMS message to: " + userPhone + " and exiting program.")

        # closes the connection and quits the program
        con.close()
        sys.exit()


# gets the current version of Awesome Miner and saves to the currentVersion variable
def get_current_version():
    global currentVersion

    content = urllib.request.urlopen(URL).read()
    soup = BeautifulSoup(content, 'html.parser')
    lines = soup.prettify().split("\n")
    currentVersion = lines[0].strip()


print("Starting Awesome Miner Update Checker.")

#gets the current version of Awesome Miner
get_current_version()
print("Getting current version of Awesome Miner: {}.".format(currentVersion))

# opens the Input Data text document and saves the variables
f = open("Input Data.txt")
print("Opening Input Data.txt.")

if not os.path.exists("Input Data.txt"):
    print("Input Data.txt cannot be found. Ensure it is in the same location as this program.")
    sys.exit()

userPhone = f.readline().strip()  # first line is the number to send the message to
minerPhone = f.readline().strip()  # second line is the from number
accountSID = f.readline().strip()  # third line is the account SID from Twilio
authToken = f.readline().strip()  # fourth line is the authentication token from Twilio

#checks to ensure the variables are not empty, and exits the program if so
if userPhone == "" or minerPhone == "" or accountSID == "" or authToken == "":
    print("Invalid input format.\nLine 1: receive phone number.\nLine 2: sending phone number.\n"
          "Line 3: Account SID.\nLine 4: Authentication Token.")
    f.close()
    sys.exit()

# checks the length of US phone number: 1 xxx xxx xxxx
if len(userPhone) != 11 or len(minerPhone) != 11:
    print("Invalid phone number. Ensure format is: xxxxxxxxxxx and includes the country code of 1 for US.")
    f.close()
    sys.exit()

f.close()


# opens connection to the database
con = sqLite.connect('Awesome-Miner-DB.db')
c = con.cursor()
print("Connecting to the database.")

# checks to see if INFO table already exists
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='INFO' ''')
if c.fetchone()[0] == 1:  # checks if the database exists
    pass
else:  # database does not exist, so it creates a database and creates the INFO table
    c.execute(
        "CREATE TABLE INFO (userPhone INTEGER, minerPhone INTEGER, version TEXT, accountSID TEXT, authToken TEXT)"
    )
    print("INFO table does not exist, creating INFO table.")
    sql = "INSERT INTO INFO (userPhone, minerPhone, version, accountSID, authToken) VALUES (?, ?, ?, ?, ?) "
    data = [
        (userPhone, minerPhone, currentVersion, accountSID, authToken)
    ]
    c.executemany(sql, data)
    con.commit()  # commits the changes

con.close()

print("Checking for updates at 0700.")
# will check for updates every day at 0700
schedule.every().day.at("07:00").do(check_for_updates)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    pass