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



try:
    while(True):
        print('Write the desired ID!')
        id = int(input())
        festo_connection.writeCarrierID(ip, id)
        print('The ID is now: ', festo_connection.getCarrierID(ip))
except KeyboardInterrupt:
        print('interrupted!')