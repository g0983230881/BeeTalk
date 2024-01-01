import paho.mqtt.client as mqtt
import demjson
import time, random, requests
import DAN
from flask import Flask,render_template,request,jsonify
import pymysql,datetime
ServerURL = 'https://asia.iottalk.tw/'      #with non-secure connection
    #ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'NBB' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='BEEE'
#DAN.profile['df_list']=['Temp_I','Temp_O']
DAN.profile['df_list']=['IN_Temp_I','IN_Temp_O','IN_Humid_I','IN_Humid_O',
'OUT_Temp_I','OUT_Temp_O','OUT_Humid_I','OUT_Humid_O','WEIGHT_I','WEIGHT_O','VOL_I','VOL_O','RSSI_I','RSS_O']
#DAN.profile['df_list']=['IN_Temp_I','IN_Temp_O','IN_Humid_I','IN_Humid_O',
#'OUT_Temp_I','OUT_Temp_O','OUT_Humid_I','OUT_Humid_O','WEIGHT_I','WEIGHT_O','VOL_I','VOL_O','RSSI_I','RSS_O',
#'IN_COUNT_I','OUT_COUNT_I','IN_COUNT_O','OUT_COUNT_O']
DAN.profile['d_name']= 'NBB' 
DAN.device_registration_with_retry(ServerURL, Reg_addr)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("bee_talk/bee_talk")

def on_message(client, userdata, msg):
    try:
        print(msg.topic+" " + ":" + str(msg.payload, encoding = "utf-8"))
        message =demjson.decode(str(msg.payload, encoding = "utf-8"))
    except:
        print("IS NOT JSON")
    #print(message)
    #print( message['temp'])
    #print( message['humid'])
    try:
        IDF_data=message['out_temp']
        IDF_data2=message['out_hum']
        IDF_data3=message['in_temp']
        IDF_data4=message['in_hum']
        IDF_data5=message['weight']
        IDF_data6=message['vol']
        IDF_data7=message['rssi']
        #IDF_data8=message['in_count']
        #IDF_data9=message['out_count']
        DAN.push('OUT_Temp_I',IDF_data)
        DAN.push('OUT_Humid_I',IDF_data2)
        DAN.push('IN_Temp_I',IDF_data3)
        DAN.push('IN_Humid_I',IDF_data4)
        DAN.push('WEIGHT_I',IDF_data5)
        DAN.push('VOL_I',IDF_data6)
        DAN.push('RSSI_I',IDF_data7)
        #DAN.push('IN_COUNT_I',IDF_data8)
        #DAN.push('OUT_COUNT_I',IDF_data9)
    except:
        print("IS NOT JSON")
        #print('IS NOT JSON')
    #DAN.push('Temp_I',IDF_data)
    #DAN.push('Humid_I',IDF_data2)
    #ODF_data = DAN.pull ('Temp_O')
    #if(ODF_data != None):
    #    print(ODF_data[0])

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("49.159.93.218", 1883, 60)
client.loop_forever()
