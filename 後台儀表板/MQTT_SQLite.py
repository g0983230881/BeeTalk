import paho.mqtt.client as mqtt
import datetime,sqlite3
import demjson

DB_File = "AS.db"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("bee_talk/bee_talk")
def on_message(client, userdata, msg):
    datetime_str = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    try:
        message =demjson.decode(str(msg.payload, encoding = "utf-8"))
        print(message)
    except:
        print("IS NOT JSON")
    conn = sqlite3.connect(DB_File)
    c = conn.cursor()
    cursor = c.execute("select * from DATA2 order by NO desc")
    #cursor = d.execute("select * from DATA2 order by NO desc")
    r=cursor.fetchone()
    #print(r)
    KEY=0
    if r!=None:
        if len(r)==0:
            KEY=1
        else:
            KEY=r[0]+1
    else:
        KEY=1
    try:    
        c.execute("insert into DATA2(NO,OUT_TEMP,OUT_HUMID,IN_TEMP,IN_HUMID,WEIGHT,VOL,RSSI,DATETIME) VALUES("+str(KEY)+
        ",'"+str(message['out_temp'])+"','"+str(message['out_hum'])+"','"+str(message['in_temp'])+"' ,'"+str(message['in_hum'])+"' ,'"+str(message['weight'])+"' ,'"+str(message['vol'])+"' ,'"+str(message['rssi'])+"' ,'"+datetime_str+"')")
        #c.execute("insert into DATA2(NO,IN_TEMP,IN_HUMID,DATETIME) VALUES("+str(KEY)+
        #",'"+str(message['in_temp'])+"','"+str(message['in_hum'])+"','"+datetime_str+"')")
    except:
        print("IS NOT JSON")
    conn.commit()
    cursor.close()
    print("Table created successfully")
    conn.close()#

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("49.159.93.218", 1883, 60)
client.loop_forever()