import sys
import time
import firebase_admin
from firebase_admin import db
import json
sys.path.insert(0, "..")
from opcua import Client, ua
from festo_opcua import simpleConnect

#IPs for each festo module
ip = '172.20.1.1' #Manual packing module STPLC_08
ip2 = '172.20.13.1' #Manual workstation STPLC_09

festo_connection = simpleConnect()
   
festo_connection.engageStopper(ip)
festo_connection.engageStopper(ip2)
festo_connection.startConveyor(ip)
festo_connection.startConveyor(ip2)
   
   
check = festo_connection.checkPallet(ip)
check2 = festo_connection.checkPallet(ip2)

while 1:
    if check is True:
        print(festo_connection.getCarrierID(ip))
        festo_connection.releaseStopper(ip)
        time.sleep(0.2)
        festo_connection.engageStopper(ip)

    if check2 is True:
        print(festo_connection.getCarrierID(ip2))
        festo_connection.releaseStopper(ip2)
        time.sleep(0.2)
        festo_connection.engageStopper(ip2)
    check = festo_connection.checkPallet(ip)
    check2 = festo_connection.checkPallet(ip2)
    time.sleep(0.2)