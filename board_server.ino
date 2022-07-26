#include <Arduino.h>
#include <ArduinoJson.h>
StaticJsonDocument<256> doc;
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WebSocketsServer.h>
#include <ESP8266mDNS.h>
#include <Hash.h>


#define USE_SERIAL Serial

int motor_a1 = 13;
int motor_a2 = 12;
int motor_b1 = 8;
int motor_b2 = 7;
int red = 5;
int green = 4;
int yellow = 14;
int blue = 12;
ESP8266WiFiMulti WiFiMulti;
WebSocketsServer webSocket = WebSocketsServer(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

  switch (type) {
    case WStype_DISCONNECTED:
      USE_SERIAL.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED:

      webSocket.sendTXT(num, "Connected");
      connectedPayLoadFunction(payload);


      break;
    case WStype_TEXT:
      getPayloadFunction(payload);
      break;
  }

}

void setup() {
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(green, OUTPUT);
  USE_SERIAL.begin(115200);
  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();
  for (uint8_t t = 4; t > 0; t--) {
    USE_SERIAL.printf("[SETUP] BOOT WAIT %d...\n", t);
    USE_SERIAL.flush();
    delay(1000);
  }
  //WiFiMulti.addAP("Galaxy A017411", "00000000");
  //WiFiMulti.addAP("MobileWiFi-8b66", "16416542");
  //WiFiMulti.addAP("Frigo Internet", "Zivl2308");
  
  WiFiMulti.addAP("itel P13", "mummyboy1");
  //WiFiMulti.addAP("TechSpace", "#Thinksmart?");
  while (WiFiMulti.run() != WL_CONNECTED) {
    delay(100);
  }

  // start webSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  if (MDNS.begin("esp8266")) {
    USE_SERIAL.println("MDNS responder started");
    Serial.println(WiFi.localIP());
  }
  // Add service to MDNS
  MDNS.addService("ws", "tcp", 81);



}

void loop() {
  webSocket.loop();

}


void connectedPayLoadFunction(uint8_t * payload) {
  String payload1 = (char * )payload;
  Serial.println(payload1);
}


void getPayloadFunction(uint8_t * payload) {
  String payload1 = (char * )payload;

  Serial.println(payload1);
  //if left is clicked
  if (payload1 == "Left")
  {
    digitalWrite(yellow, HIGH);
  }

  
  //if right is clicked
  if (payload1 == "Right")
  {
    digitalWrite(blue, HIGH);
  }




  //if forward is clicked
  if (payload1 == "Forward")
  {
    digitalWrite(green, HIGH);
  }



  
  //if Back is clicked
  if (payload1 == "Back")
  {
    digitalWrite(red, HIGH);
  }

  if (payload1 == "released")
  {
    digitalWrite(red, LOW);
    digitalWrite(yellow, LOW);
    digitalWrite(blue, LOW);
    digitalWrite(green, LOW); 
    
    
  }


}

