# IoT-project
IoT project for Software Engineering course (SKEL413) on Flood Monitoring System

## Problem Statement
Flood is a major known natural disaster that causes a huge amount of loss to the environment and living beings. So in these conditions, it is most crucial to get the emergency alerts of water level status at river beds in different conditions. In this project, the objective is to sense the water levels at river beds and check whether they are at a normal condition or not.

## System Architecture
![system architecture](https://user-images.githubusercontent.com/94040083/147046684-43c0744f-665b-4bf8-b4fe-7f2ab068594a.jpg)

## Sensor
The sensor we use is HC-SR04 Ultrasonic Sensor. The ultrasonic sensor works on the principle of ultrasound waves which is used to determine the distance to an object. 

![image](https://user-images.githubusercontent.com/94040083/147049018-50cd8e7e-518d-4c57-b478-600a1af922a5.png)

<details>
<summary>Code</summary>
<code style="white-space:nowrap;">
  
#include "ThingSpeak.h"

#include <ESP8266WiFi.h>
  
const int trigPin1 = D1;
  
const int echoPin1 = D2;
  
#define redled D3
  
#define grnled D4
  
unsigned long ch_no = 1026389;//Replace with Thingspeak Channel number
  
const char * write_api = "XK88XXXXXXX";//Replace with Thingspeak write API
  
char auth[] = "fu0o5JaLXXXXXXXXXXXXXXXX";
  
char ssid[] = "admin";
  
char pass[] = "";
  
unsigned long startMillis;
  
unsigned long currentMillis;
  
const unsigned long period = 10000;
  
WiFiClient  client;
  
long duration1;
  
int distance1;
  
void setup()
  
{
  
  pinMode(trigPin1, OUTPUT);
  
  pinMode(echoPin1, INPUT);
  
  pinMode(redled, OUTPUT);
  
  pinMode(grnled, OUTPUT);
  
  digitalWrite(redled, LOW);
  
  digitalWrite(grnled, LOW);
  
  Serial.begin(9600);
  
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED)
  
  {
    delay(500);
  
    Serial.print(".");
  
  }
  
  Serial.println("WiFi connected");
  
  Serial.println(WiFi.localIP());
  
  ThingSpeak.begin(client);
  
  startMillis = millis();  //initial start time
  
}

  void loop()

  {
  
  digitalWrite(trigPin1, LOW);
  
  delayMicroseconds(2);
  
  digitalWrite(trigPin1, HIGH);
  
  delayMicroseconds(10);
  
  digitalWrite(trigPin1, LOW);
  
  duration1 = pulseIn(echoPin1, HIGH);
  
  distance1 = duration1 * 0.034 / 2;
  
  Serial.println(distance1);
  
  if (distance1 <= 4)
                    
  {
   
    digitalWrite(D3, HIGH);
                    
    digitalWrite(D4, LOW);
                    
  }
                    
  else
                    
  {
                    
    digitalWrite(D4, HIGH);
                    
    digitalWrite(D3, LOW);
                    
  }
                    
  currentMillis = millis();
                    
  if (currentMillis - startMillis >= period)
  
  {
  
    ThingSpeak.setField(1, distance1);
  
    ThingSpeak.writeFields(ch_no, write_api);
  
    startMillis = currentMillis;
  
  }
  
}

</code>
</details>




## Cloud Platform
ThingSpeak is a software which can communicate with internet enabled devices. ThingSpeak can store the data in the channel and analyze it.

## Dashboard
This is the example of the dashboard by using Thingspeak.
![image](https://user-images.githubusercontent.com/94040083/147047818-d894712b-44de-4082-84ea-07204f543a9e.png)
