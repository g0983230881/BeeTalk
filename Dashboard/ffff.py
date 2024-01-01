import time, random, requests
import DAN

ServerURL = 'https://asia.iottalk.tw/'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'RRR' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Bee'
DAN.profile['df_list']=['Humid_I','Humid_O']
DAN.profile['d_name']= 'RRR' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
#x = -1
while True:
    try:
        IDF_data = random.uniform(1, 10)
        DAN.push('Humid_I',IDF_data)
        ODF_data = DAN.pull ('Humid_O')
        if(ODF_data != None):
            print(ODF_data[0])
        #==================================

        # ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        # if ODF_data != None:
        #     print (ODF_data[0])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

