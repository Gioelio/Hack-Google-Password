# Hack-Google-Password
Simple python script for doing request for taking access token from google, if this send a valid token you found the password, this script is only for educational purpose only. I don't take any responsibility for the improper use of this code
## Installation and usage
You must install python 3.* for use this script, first you executed this, you must modify settings.cfg file and in there the only field that you have to modify is gmail, in there you will put email that you want to test without any characters (i.e. ",',...).
Then for start the script you must open a simple terminal, go the directory and then write
```
python3 generator.py
```
Then the script will ask you some information of the account that you want to test and then it will start a multithread that mix the words and the numbers to try to find the correct password, I also inform you that this script works also the account have verify in two steps with gmail and this script doesn't send any information to this account, but doesn't work with verify in two steps with sms, also in this case if you try the password for the account and you are lucky and found the password in one of the request, google server doesn't infrom the owner of the account.
Summing, if the account have any type of verify in two steps active the google server doesn't send him any message, if the account tested doesn't have any protection you will found the password in a new created file.
During the execution you can stop the program with ctrl+c and reexecute then without losing the tryied password, because the failed attempts will saved into a file with the name of the account.
Whereas this script use multithreading, I advice you to execute this on a desktop computer.
I will inform you that for the realization of this script I will inspired by this: https://github.com/EliteAndroidApps/WhatsApp-GD-Extractor
that allows you to download whatsapp backup without have the phone (for decrypt the chat you must have the token that is inside the phone, but for see the images/video folder you must only follow the instruction of this script).
In the end I inform you that this script is a beta version and it can have some problem
