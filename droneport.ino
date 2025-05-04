#include <WiFi.h>
#include <FastLED.h>
#include "GyverStepper.h"

#define NUM_LEDS 256 
#define PIN 4 // LED
#define buz 1 //BUZZER

const char* ssid = "ASUS_20";
const char* password =  "harmony_9957";

WiFiServer wifiServer(80);
CRGB leds[NUM_LEDS];
GStepper< STEPPER4WIRE> stepperL(2038, 5, 7, 6, 8);  //Если смотреть на дронпорт со стороны матрицы - Левый
GStepper< STEPPER4WIRE> stepperR(2038, 10, 18, 9, 19);  //Если смотреть на дронпорт со стороны матрицы - Правый



void setup() 
{
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {delay(500);}
  wifiServer.begin();

  stepperL.autoPower(true);
  stepperR.autoPower(true);
  stepperL.setMaxSpeed(400);
  stepperR.setMaxSpeed(400);
  stepperL.reverse(true);

  FastLED.addLeds <WS2812, PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(50);
  ready();
}


void ready()
{
  FastLED.showColor(CRGB::Green);
  tone(buz, 1300);
  delay(500);
  noTone(buz);
  delay(500);
  tone(buz, 1500);
  delay(500);
  noTone(buz);
  tone(buz, 1700);
  delay(500);
  noTone(buz);
  FastLED.clear();
  FastLED.show();
}


void verx()
{
  FastLED.clear(); 
  for(int x=71; x<184;) { leds[x] = CRGB::Green; x=x+16;}
  for(int x=72; x<185;) { leds[x] = CRGB::Green; x=x+16;}
  leds[169] = CRGB::Green;//verx
  leds[166] = CRGB::Green;
  leds[149] = CRGB::Green;
  leds[154] = CRGB::Green;
  FastLED.show();

}


void vniz()
{
  FastLED.clear(); 
  for(int x=71; x<184;){ leds[x] = CRGB::Red; x=x+16;}
  for(int x=72; x<185;){ leds[x] = CRGB::Red; x=x+16;}
  leds[86] = CRGB::Red;//vniz
  leds[89] = CRGB::Red;
  leds[106] = CRGB::Red;
  leds[101] = CRGB::Red;
  FastLED.show();
}


void batka()
{
  FastLED.clear(); 
  for (int x =149; x<158; x++) {leds[x] = CRGB::Red;}  
  for (int x =98; x<107; x++) {leds[x] = CRGB::Red;}  
  leds[125] = CRGB::Red;
  leds[130] = CRGB::Red;
  leds[115] = CRGB::Red;
  leds[116] = CRGB::Red;
  leds[117] = CRGB::Red;
  leds[138] = CRGB::Red;
  leds[139] = CRGB::Red;
  leds[140] = CRGB::Red;
  FastLED.show();
}

// КАРТИНКИ


void open()
{
  stepperR.setTargetDeg(360); 
  stepperL.setTargetDeg(360); 
}


void close()
{
  stepperR.setTargetDeg(0); 
  stepperL.setTargetDeg(0);
}


void zvuk() 
{
  tone(buz, 1900);
  delay(500);
  noTone(buz);
  delay(500);
  tone(buz, 1900);
  delay(500);
  noTone(buz);
}


void ledoff()
{
  FastLED.clear(); 
  FastLED.show();
}


void loop() 
{  
  stepperL.tick();
  stepperR.tick();

  WiFiClient client = wifiServer.available();

  if (client.connected())
     {
     if (client.available()>0) 
        {
          char msg = client.read();
          int data = msg -'0' ;

          switch(data)
                {
                case 1: client.write(1); open(); break; //open  

                case 2: client.write(1); close(); break;  //close
                
                case 3: 
                      verx(); 
                      zvuk(); 
                      open(); 
                      while(stepperL.tick() && stepperR.tick()) {}            //takeoff
                      client.write(1); break;
                
                case 4: 
                      vniz(); 
                      zvuk(); 
                      close();
                      while(stepperL.tick() && stepperR.tick()) {}
                      client.write(1); break;     //land
                
                case 5: client.write(1); batka();  break;                    //charge
                
                case 6: client.write(1); ledoff(); close(); break;          //off

                  default: break;
                }
         
        }
     }     
}
