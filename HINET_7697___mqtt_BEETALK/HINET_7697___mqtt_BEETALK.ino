//7697 接收資料傳送至mqtt 溫濕度 ＆ 光（可見光/IR/UV)
#include <Wire.h>
#include "Arduino.h"
//#include "SI114X.h"

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <LWiFi.h>
#include <PubSubClient.h>
#include <SPI.h>

#define DHTPIN1 2     // IN  Digital pin connected to the DHT sensor 
#define DHTPIN2 3     // OUT  Digital pin connected to the DHT sensor 
//SI114X SI1145 = SI114X();

//重量感測器
#include "HX711.h"
// 接線設定
const int DT_PIN = 5;
const int SCK_PIN = 4;
const int scale_factor = -24; //比例參數，從校正程式中取得
HX711 scale;

const int mqtt_led = 15;     // MQTT確認狀態燈


//補糖水設定
const int buttonPin = 8;     // 糖水截止開關
const int pump =  7;      //補糖水馬達.   7是內建LED pin
int pumpState = 0;
int buttonState = 0;      //截止開關狀態
int test=0;

// Uncomment the type of sensor in use:
//#define DHTTYPE    DHT11     // DHT 11
#define DHTTYPE1    DHT22     // DHT 22 (AM2302)
#define DHTTYPE2    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)
//DHT dht(2, DHT11);
DHT_Unified dht2(DHTPIN1, DHTTYPE1);  // IN
DHT_Unified dht1(DHTPIN2, DHTTYPE2);  // OUT

#define bee_talk "bee_talk/bee_talk"
#define humidity_topic "20220707/bee_sensor/humidity"
#define temperature_topic "20220707/bee_sensor/temperature"
#define rain_topic "20220707/bee_sensor/rain"
#define total_topic "20220707/bee_sensor/total"

//#define vis_topic "20120123/bee_sensor/vis"
//#define ir_topic "20120123/bee_sensor/ir"
//#define uv_topic "20120123/bee_sensor/uv"

// 儲存訊息的字串變數
String msgStr = "";
// 儲存字元陣列格式的訊息字串（參閱下文說明）
char json[105];

//設定mqtt
const char clientID[] = "bee"; //ID記得跟別人不一樣
//const char* ssid = "POP";
//const char* password = "12345678";
//const char* ssid = "WU";
//const char* password = "0a56fa6261";
const char* ssid = "YTS-PC";
const char* password = "r0843010";
const char* mqtt_server = "49.159.93.218";
//const char* mqtt_server = "broker.hivemq.com";
//const char* mqtt_server = "mqttgo.io";

char message[256];
WiFiClient wificlient; //宣告WiFiClient
PubSubClient client(wificlient);

int led = 5;  //ledP
int fun = 4;  //風扇


int rain_temp=0;
int rain_temp1=0;
int rain_temp2=0;
int total = 16;  //計算
int total_temp=0;
int total_temp1=0;
int total_temp2=0;
int button = 10;  //按鈕


float pwm_cmd = 0;

void callback(char* topic, byte* payload, unsigned int length){
  /*
  //LED
  if(strcmp(topic, "home/mode20220707_1") == 0 ) {    //收到吻合主題
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i=0;i<length;i++) {
      Serial.print((char)payload[i]);
      message[i]=payload[i];
    }
    if(atoi(message) == 1 ) { digitalWrite(led, HIGH);}      //'1'點亮led
    else if(atoi(message) == 0) { digitalWrite(led, LOW);} //'2'熄滅led
    }
    */
  
  //保護遮罩
  if(strcmp(topic, "bee_talk/mesh") == 0 ) {    //收到吻合主題
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i=0;i<length;i++) {
      Serial.print((char)payload[i]);
      message[i]=payload[i];
    }
    if(atoi(message) == 1 ) { digitalWrite(fun, HIGH);}      //'1'點亮led
    else if(atoi(message) == 2) { digitalWrite(fun, LOW);} //'2'熄滅led
    }
    
  //泵浦
  if(strcmp(topic, "bee_talk/sugar") == 0 ) {    //收到吻合主題
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i=0;i<length;i++) {
      Serial.print((char)payload[i]);
      message[i]=payload[i];
    }
    if(atoi(message) == 1 ) { digitalWrite(pump, HIGH);}      //'1'點亮led
    else if(atoi(message) == 0) { digitalWrite(pump, LOW);} //'2'熄滅led
    }    
    
}




void setup() {
  Serial.begin(115200);
  Serial.println("測試");
  Serial.println("Beginning Si1145!");

  pinMode(total, INPUT);
  pinMode(button, INPUT);  

  //糖水截止開關
  pinMode(buttonPin, INPUT); 


  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);  //當ESP32接收到訂閱主題訊息時執行對應函式


  // Initialize device.溫濕度感測器
  dht1.begin();
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht1.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht1.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));

  //重量感測器
  Serial.println("HX-711 Initializing the scale");
  scale.begin(DT_PIN, SCK_PIN);
  Serial.println("Before setting up the scale:"); 
  Serial.println(scale.get_units(5), 0);  //未設定比例參數前的數值
  scale.set_scale(scale_factor);       // 設定比例參數
  scale.tare();               // 歸零
  Serial.println("After setting up the scale:"); 
  Serial.println(scale.get_units(5), 0);  //設定比例參數後的數值
  Serial.println("Readings:");  //在這個訊息之前都不要放東西在電子稱上
  Serial.println(F("------------------------------------"));
  
}

void setup_wifi() {
  delay(10);
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
    if(client.connect(clientID)) {    //正確的物件名稱（name)
    //if(client.connect("49.159.95.123")) {    //正確的物件名稱（name)  
    //if(client.connect("mqttgo.io")) {    //正確的物件名稱（name) 
      Serial.println("connected");
      //client.subscribe("home/#");    //正確的主題（topic)
      //client.subscribe("bee_talk");    //正確的主題（topic)
      digitalWrite(mqtt_led, HIGH);
    }
    else{
      
      setup_wifi();
      Serial.print("連線失敗, rc=");
      Serial.println(client.state());
      Serial.println("5秒後重新連線...");
      delay(5000);
    }
  }
}

long lastMsg = 0;
long lastMsg1 = 0;








void loop() {
  if(!client.connected()) {   //如果未連結MQTT則執行MQTT連線
    mqtt_reconnect();
    //client.subscribe("home/#");    //正確的主題（topic)
    client.subscribe("bee_talk/#");    //正確的主題（topic)
  }
  client.loop();   //保持MQTT連線

  long now = millis(); //傳送訊息計數用

  //讀取糖水開關
  //buttonState = digitalRead(buttonPin);
  //if (buttonState == LOW) {
    //糖水邦浦停止
    //digitalWrite(pump, LOW);
  //} 




  if((digitalRead(button)==0)&(total_temp1==1)){
    total_temp1=0;
    total_temp=total_temp+1;
    digitalWrite(pump, LOW);
  }


  if (now - lastMsg >5000){
    //Serial.println(rain_temp);
    //Serial.println(total_temp);
    //每隔5秒讀取溫濕度
    lastMsg = now;

    // Get temperature event and print its value.
    sensors_event_t event;
    dht1.temperature().getEvent(&event);
    float newTemp1 = event.temperature; 
    dht2.temperature().getEvent(&event);
    float newTemp2 = event.temperature;
    // Get humidity event and print its value.
    dht1.humidity().getEvent(&event);
    float newHum1 = event.relative_humidity;
    dht2.humidity().getEvent(&event);
    float newHum2 = event.relative_humidity;


    
    Serial.print("//--------------------------------------//\r\n");
    if (isnan(event.temperature)) {
      Serial.println(F("Error reading temperature!"));
    }
    else {
      Serial.print(F("Temperature: "));
      Serial.print(newTemp1);
      Serial.println(F("°C"));
      //發佈溫度訊息
      //client.publish(temperature_topic, String(newTemp1).c_str(), true);
      //client.publish(bee_talk, String(newTemp).c_str(), true);
    }    

    if (isnan(event.relative_humidity)) {
      Serial.println(F("Error reading humidity!"));
    }
    else {
      Serial.print(F("Humidity: "));
      Serial.print(newHum1);
      Serial.println(F("%"));
      //發佈濕度訊息
      //client.publish(humidity_topic, String(newHum1).c_str(), true);
    }
    

    

    
    Serial.print("//--------------------------------------//\r\n");



    //重量偵測
    scale.power_up();               // 結束睡眠模式
    //float weight=((scale.get_units(10)+1713)/1000);
    float weight=((scale.get_units(10))/1000);
    if (weight<=0){
      weight=0;
      }
    
    scale.power_down();             // 進入睡眠模式
    //delay(1000);

    //偵測電壓
    int V1 = analogRead(A0);
    //從A0口讀取電壓資料存入剛剛創建整數型變數V1，類比口的電壓測量範圍為0-2.5V 返回的值為0-4095
    float vol = V1*((2.5 / 4095.0)*2)+0.37;

    //網路信號            
    long rssi = WiFi.RSSI();
    if (rssi==0){
       digitalWrite(mqtt_led, LOW);
    }



    //-------------------------發佈資料------------------------
    // 建立MQTT訊息（JSON格式的字串）
    msgStr = msgStr + "{\"out_temp\":" + newTemp1 + ",\"out_hum\":" + newHum1 + ",\"in_temp\":" + newTemp2 + ",\"in_hum\":" + newHum2 + ",\"weight\":" + weight + ",\"vol\":" + vol + ",\"rssi\":" + rssi + "}";
    // 把String字串轉換成字元陣列格式
    msgStr.toCharArray(json, 105);
    // 發布MQTT主題與訊息
    client.publish(bee_talk, json);
    // 清空MQTT訊息內容
    Serial.println(msgStr);
    msgStr = "";


    
    
  }


}
