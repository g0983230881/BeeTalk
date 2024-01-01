import paho.mqtt.client as mqtt
import demjson
import time, random, requests
import DAN
from flask import Flask,render_template,request,jsonify
ServerURL = 'https://asia.iottalk.tw/'      #with non-secure connection
    #ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'RRR' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Bee'
#DAN.profile['df_list']=['Humid_I','Humid_O']
DAN.profile['df_list']=['Humid_I','Humid_O','Temp_I','Temp_O']
DAN.profile['d_name']= 'RRR' 
DAN.device_registration_with_retry(ServerURL, Reg_addr)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("NIU")
def on_message(client, userdata, msg):
    #print(msg.topic+" " + ":" + str(msg.payload, encoding = "utf-8"))
    message =demjson.decode(str(msg.payload, encoding = "utf-8"))
    #print(message)
    #print( message['temp'])
    #print( message['humid'])
    IDF_data=message['humid']
    IDF_data2=message['temp']
    DAN.push('Humid_I',IDF_data)
    DAN.push('Temp_I',IDF_data2)
    ODF_data = DAN.pull ('Humid_O')
    ODF_data2 = DAN.pull ('Temp_O')
    if(ODF_data != None):
        print(ODF_data[0])
    if(ODF_data2 != None):
        print(ODF_data2[0])
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("203.145.202.162", 1883, 60)
client.loop_forever()
