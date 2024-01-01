import time, random, requests
import DAN
from flask import Flask,render_template,request,jsonify
app = Flask(__name__)
ServerURL = 'https://asia.iottalk.tw/'      #with non-secure connection
    #ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'RRR' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Bee'
DAN.profile['df_list']=['Humid_I','Humid_O']
DAN.profile['d_name']= 'RRR' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
@app.route('/') #路由
def index():
    return 'Hello World!'

@app.route('/NIUPOST',methods=['POST']) #路由
def NIUGET():
    #print(request.headers)
    print(request.json)
    #print("溫度:")
    #print(request.args.get('temp'))#獲取http get中的temp數值
    #print("濕度:")
    #print(request.args.get('humid'))#獲取http get中的humid數值
    while True:
        try:
            #IDF_data = request.args.get('humid')
            IDF_data = (request.json['humid'])           #random.uniform(1, 10)
            DAN.push('Humid_I',IDF_data)
            ODF_data = DAN.pull ('Humid_O')
            if(ODF_data != None):
                print(ODF_data[0])
    #        #==================================
    #
    #        # ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
    #        # if ODF_data != None:
    #        #     print (ODF_data[0])#
    #
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    

    time.sleep(5)
    return ""

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)


#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
#x = -1






    

