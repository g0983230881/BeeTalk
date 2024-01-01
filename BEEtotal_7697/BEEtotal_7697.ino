//#include <LiquidCrystal_PCF8574.h>
//LiquidCrystal_PCF8574 lcd(0x27);  // 設定i2c位址
//蜂數器 7697 接收資料傳送至mqtt


#include <LWiFi.h>
#include <PubSubClient.h>
#include <SPI.h>


#define bee_talk "bee_talk/in_out"
#define bee_in "bee_talk/in"
#define bee_out "bee_talk/out"

// 儲存訊息的字串變數
String msgStr = "";
// 儲存字元陣列格式的訊息字串（參閱下文說明）
char json[105];

//const char* ssid = "WU";
//const char* password = "0a56fa6261";
const char* ssid = "YTS-PC";
const char* password = "r0843010";
//const char* mqtt_server = "broker.hivemq.com";
//const char* mqtt_server = "mqttgo.io";
const char* mqtt_server = "49.159.93.218";

WiFiClient wificlient; //宣告WiFiClient
PubSubClient client(wificlient);


//注意腳位定義TX RX使用LCD顯示器必須移除才能燒錄
//LCD P0 P8 P9 P5無法使用 通訊PORT P1無法使用 6  
//#define betton1 1 // 後面宣告
//#define betton5 7 // 後面宣告
#define betton2 2
#define betton3 3
#define betton4 4

#define betton9 10
#define betton10 11
#define betton11 12
#define betton12 13
#define betton13 14
#define betton14 15
#define betton15 16 
#define betton16 17

 

int comb_betton_add(int ,int ,int* ,int* ,int* ,int* ,int* ,int* ,int* ,int* );

int ii1=0,ij1=0,ik1=0,il1=0,oi1=0,oj1=0,ok1=0,ol1=0;
int ii2=0,ij2=0,ik2=0,il2=0,oi2=0,oj2=0,ok2=0,ol2=0;
int ii3=0,ij3=0,ik3=0,il3=0,oi3=0,oj3=0,ok3=0,ol3=0;
int ii4=0,ij4=0,ik4=0,il4=0,oi4=0,oj4=0,ok4=0,ol4=0;
int ii5=0,ij5=0,ik5=0,il5=0,oi5=0,oj5=0,ok5=0,ol5=0;
int ii6=0,ij6=0,ik6=0,il6=0,oi6=0,oj6=0,ok6=0,ol6=0;
int ii7=0,ij7=0,ik7=0,il7=0,oi7=0,oj7=0,ok7=0,ol7=0;
int ii8=0,ij8=0,ik8=0,il8=0,oi8=0,oj8=0,ok8=0,ol8=0;
int IN=0,OUT=0,Total=0;

void setup() {
//  lcd.begin(16, 2); // 初始化LCD
//  lcd.setBacklight(255);
//  lcd.clear();
  Serial.begin(115200);
  Serial.print("Total= ");
  
  //pinMode(betton1, INPUT);

  //pinMode(9, INPUT); //
  //pinMode(6, INPUT); //
  pinMode(betton2, INPUT);
  pinMode(betton3, INPUT);
  pinMode(betton4, INPUT);
//  pinMode(betton5, INPUT);
//  pinMode(betton6, INPUT);

  pinMode(betton9, INPUT);
  pinMode(betton10, INPUT);
  pinMode(betton11, INPUT);
  pinMode(betton12, INPUT);
  pinMode(betton13, INPUT);
  pinMode(betton14, INPUT);
  pinMode(betton15, INPUT);
  pinMode(betton16, INPUT); 

  
  //pinMode(betton17, INPUT);
  //pinMode(betton18, INPUT);


  

  
  Serial.println("測試");
  setup_wifi();
  client.setServer(mqtt_server, 1883); 
}

void setup_wifi() {
  delay(1000);
  //連接WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);//連接WiFi

  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);                //持續連接直到連上WiFi
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi 已連接！");
  Serial.print("WiFi IP 位置 ： ");
  Serial.println(WiFi.localIP());  //顯示IP位置
  //顯示WiFi信號強度
  long rssi = WiFi.RSSI();
  Serial.print("信號強度(RSSI) : ");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void mqtt_reconnect() {
  while(!client.connected()) {
    Serial.print("嘗試連線MQTT 連線中...");    //嘗試連線MQTT
    if(client.connect("MQTT_client1")) {    //正確的物件名稱（name)
      Serial.println("connected");
      //client.subscribe("home/#");    //正確的主題（topic)
  
    }
    else{
      Serial.print("連線失敗, rc=");
      Serial.print(client.state());
      Serial.println("5秒後重新連線...");
      delay(4000);
    }
  }
}

float lastMsg=0;


void loop() {
  if(!client.connected()) {   //如果未連結MQTT則執行MQTT連線
    mqtt_reconnect();
  }
  client.loop();   //保持MQTT連線

  long now = millis();
  if (now - lastMsg >5000){
    //每隔5秒讀取
    lastMsg = now;

    
    //-------------------------發佈資料------------------------
    // 建立MQTT訊息（JSON格式的字串）
    msgStr = msgStr + "{\"bee_in\":" + IN + ",\"bee_out\":" + OUT  + "}";
    // 把String字串轉換成字元陣列格式
    msgStr.toCharArray(json, 105);
    // 發布MQTT主題與訊息
    client.publish(bee_talk, json);
    // 清空MQTT訊息內容
    Serial.println(msgStr);
    msgStr = "";

    Serial.print ("IN:");
    Serial.println(IN);
    //發佈溫度訊息
    //client.publish(bee_in, String(IN).c_str(), true);
    IN=0;

    Serial.print ("OUT:");
    Serial.println(OUT);
    //發佈濕度訊息
    //client.publish(bee_out, String(OUT).c_str(), true);
    OUT=0;


    
  }
  /*
  //lcd.clear();
  lcd.setCursor(0, 0);  //設定游標位置 (字,行)
  lcd.print(" IN=");
  lcd.print(IN);
  lcd.setCursor(0, 1);
  lcd.print("OUT=");
  lcd.print(OUT);
  //lcd.setCursor(0, 1);
  //lcd.print("Total=");
  //lcd.print(Total);
  //lcd.clear();
  */



  /*
  Serial.print("Total= ");
  Serial.print(Total);
  Serial.print(", IN= ");
  Serial.print(IN);
  Serial.print(" , OUT= ");
  Serial.println(OUT);
  */
    /*
    Serial.print ("1:");
    Serial.println(betton1);
    Serial.print ("2:");
    Serial.println(betton2);
    Serial.print ("3:");
    Serial.println(betton3);
    Serial.print ("4:");
    Serial.println(betton4);
    Serial.print ("5:");
    Serial.println(betton5);
    Serial.print ("6:");
    Serial.println(betton6);
    Serial.print ("7:");
    Serial.println(betton7);
    Serial.print ("8:");
    Serial.println(betton8);
    Serial.print ("9:");
    Serial.println(betton9);
    Serial.print ("10:");
    Serial.println(betton10);
    Serial.print ("11:");
    Serial.println(betton11);
    Serial.print ("12:");
    Serial.println(betton12);
    Serial.print ("13:");
    Serial.println(betton13);
    Serial.print ("14:");
    Serial.println(betton14);
    Serial.print ("15:");
    Serial.println(betton15);
    Serial.print ("16:");
    Serial.println(betton16);
    */   

  //comb_betton_add(betton1,betton2,&ii1,&ij1,&ik1,&il1,&oi1,&oj1,&ok1,&ol1);
  comb_betton_add(betton2,betton3,&ii2,&ij2,&ik2,&il2,&oi2,&oj2,&ok2,&ol2);
  //comb_betton_add(digitalRead(9),digitalRead(6),&ii3,&ij3,&ik3,&il3,&oi3,&oj3,&ok3,&ol3);
  //comb_betton_add(betton7,betton8,&ii4,&ij4,&ik4,&il4,&oi4,&oj4,&ok4,&ol4);
  comb_betton_add(betton9,betton10,&ii5,&ij5,&ik5,&il5,&oi5,&oj5,&ok5,&ol5);
  comb_betton_add(betton11,betton12,&ii6,&ij6,&ik6,&il6,&oi6,&oj6,&ok6,&ol6);
  comb_betton_add(betton13,betton14,&ii7,&ij7,&ik7,&il7,&oi7,&oj7,&ok7,&ol7);
  comb_betton_add(betton15,betton16,&ii8,&ij8,&ik8,&il8,&oi8,&oj8,&ok8,&ol8);

  //Serial.print (digitalRead(betton16));
  //Serial.print (digitalRead(9));
  //Serial.print (digitalRead(6));
}


int comb_betton_add(int bettonA,int bettonB,int *ii,int *ij,int *ik,int *il,int *oi,int *oj,int *ok,int *ol){
    if (digitalRead(bettonA) == 0 && digitalRead(bettonB) == 1) {
    *ii=1;
    }
    if (*ii==1 && digitalRead(bettonA) == 0 && digitalRead(bettonB) == 0) {
    *ii=0;
    *ij=1;
    }
    if (*ij==1 && digitalRead(bettonA) == 1 && digitalRead(bettonB) == 0) {
    *ij=0;
    *ik=1;
    }
    if (*ik==1 && digitalRead(bettonA) == 1 && digitalRead(bettonB) == 1) {
    *ik=0;
    *il=1;
    }    
    //以上進入

    if (digitalRead(bettonA) == 1 && digitalRead(bettonB) == 0) {
    *oi=1;
    }
    if (*oi==1 && digitalRead(bettonA) == 0 && digitalRead(bettonB) == 0) {
    *oi=0;
    *oj=1;
    }
    if (*oj==1 && digitalRead(bettonA) == 0 && digitalRead(bettonB) == 1) {
    *oj=0;
    *ok=1;
    }
    if (*ok==1 && digitalRead(bettonA) == 1 && digitalRead(bettonB) == 1) {
    *ok=0;
    *ol=1;
    }
    //以上離開

    //以下計算數量進入
    if (*il == 1) {
    Total=Total+1;
    IN=IN+1;
    *ii=0;
    *ij=0;
    *ik=0;
    *il=0;
    *oi=0;
    *oj=0;
    *ok=0;
    *ol=0;
    }
    //以下計算數量離開
    if (*ol == 1) {
    Total=Total-1;
    OUT=OUT+1;
    *ii=0;
    *ij=0;
    *ik=0;
    *il=0;
    *oi=0;
    *oj=0;
    *ok=0;
    *ol=0;
    }

    
    
    
}
