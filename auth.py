
from functions import validateIP,requestLogin
from strings import greetingString
from log import *
from log import invalidIPLog
import traceback
import os
import logging

username = ""
execPrivPassword = ""
netDevice = {}

def Auth(swHostname):
    global username, execPrivPassword, netDevice

    os.system("CLS")
    greetingString()
    while True:
        swHostname1 = validateIP(swHostname) # Returns the validated/reachable hostname
        authLog.error(f"User {username} input the following invalid IP: {swHostname}")
        authLog.error(traceback.format_exc())
        break
        
    swHostname, username, netDevice = requestLogin(swHostname1)

    return swHostname,username,netDevice