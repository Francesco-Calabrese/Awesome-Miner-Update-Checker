# Awesome-Miner-Update-Checker
Checks for updates on the Awesome Miner Program and sends a SMS alert when updates are available.

Operation
----
This program was created for a Windows 10 environment. First obtain a Twilio account (free) - see below. Next create the Input Data text file. Using the command prompt (start -> cmd), navigate to the Awesome_Miner_Update_Checker.exe and launch. Exit the program by using Ctrl-X.

Once launched, the program will create a database (SQLite) named INFO and get the current version of Awesome Miner. Every day at 0700, it will check online (https://www.awesomeminer.com/download/setup/releaseinfo.txt) for the current version of Awesome Miner. If a new version is found, it will send a SMS message to the provided phone number. Once the SMS message is sent, the program will exit. You should update Awesome Miner and then rerun this program. 

![image](https://user-images.githubusercontent.com/96243400/164092157-cbb1e70d-9237-476f-a024-8f547ecbf739.png)

Twilio
------
You must register with Twilio to use the SMS feature (https://www.twilio.com/). This program will send SMS messages to your authenticated phone number from a Twilio phone number that is included in the free version. You must have a US phone number for this program to work.

Once registered, obtain the Account SID, Authentication Token, and Twilio Phone number for use in the Input Data Text file. See the image below.

![image](https://user-images.githubusercontent.com/96243400/164089349-7495f9d2-5d3d-4599-8429-243c5020e628.png)


Input Data.txt
----
This text file should be placed in the same location as the Awesome_Miner_Update_Checker.exe file and should contain 4 lines as follows:

The first line is the phone number that will receive the SMS message. It should be in the form 1aaabbbcccc (1 representing the US country code). Do not place any spaces or other characters between the numbers. Example: 19598381122.

THe second line is the phone number that is sending the SMS message (Twilio phone number). It should be in the same format as the receiving phone number. 

The third line is the Account SID from Twilio.

The fourth line is the Authentication Token from Twilio. 

Requirements
----
<ul>
  <li>beautifulsoup4==4.11.1</li>
  <li>certifi==2021.10.8</li>
  <li>charset-normalizer==2.0.12</li>
  <li>idna==3.3</li>
  <li>PyJWT==2.3.0</li>
  <li>pytz==2022.1</li>
  <li>requests==2.27.1</li>
  <li>schedule==1.1.0</li>
  <li>soupsieve==2.3.2.post1</li>
  <li>twilio==7.8.1</li>
  <li>urllib3==1.26.9</li>
</ul>
