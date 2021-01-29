# Hack-Google-Password [now not working for some changes in google]
Simple python script for doing request for taking access token from google, based on the word inserted from user and mixed between them automatically. If this script send a valid token you found the password, this script is only for educational purpose only. I don't take any responsibility for the improper use of this code (for now I do not ensure it will work, because google has added a system that "bans" too many requests on the same account by responding negatively even to the correct password, but with the addition of the 2 second delay it seems to work) (update: if you read this, probabily this is not working, when i have time i will fix it, if you have some solution please create a new pull request ;) ).
## Installation and usage
### Prerequisistes
1. O/S: Windows Vista, Windows 7, Windows 8, Windows 10, Mac OS X or Linux
2. python 3.* installed in your computer, if not installed: https://www.python.org/downloads/

### Usage
0. Check you if you have installed configparser and requests with this command:
```
  $ python3 -m pip install requests configparser
  ```
1. Modify setting.cfg file and write the email you want to test
2. From terminal mount the folder of the project and then type 
  ```
  $ cd Hack-Google-Password
  $ python3 generator.py
  ```
### Some info
* The script can be stopped and resumed any time because the failed attempts will saved in the file refering to relative email account
* The script don't tell to the owner that you found the password also it has the verify in two steps active
* This code works also the verify in two steps with gmail is active (but don't with verify in two steps with SMS)
* This script use multhitreading system to improve perfomance
* Auto-detect captcha request and waiting the right time before resend attemps
* On average, about 1800 requests can be sent per hour
* Problem: if the password is found the script will continue his execution, but a separated file will created with the password found

This script will be inspired by: https://github.com/EliteAndroidApps/WhatsApp-GD-Extractor

