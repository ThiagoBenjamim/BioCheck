#include <OneWire.h>
#include <DallasTemperature.h>
#define lum A0
#define umidar A1
#define umidsolo A2
#define agua A3
#define poten A4
#define lampada 2
#define leds 5
#define MIN_RAW 0 // Analog minimum value
#define MAX_RAW 1023 // Analog maximum value
#define MIN_CMD 0 // Digital minimum value
#define MAX_CMD 200 // Digital maximum value

int valorlum = 0;
int valorumidar = 0;
int valorumidsolo = 0;
int nivelagua = 0;
int valorpoten = 0;
int cmd = 0;

OneWire pino(3);
DallasTemperature barramento(&pino);
DeviceAddress sensor;

void setup(){
  Serial.begin(9600);
  pinMode(lum, INPUT);
  pinMode(umidar, INPUT);
  pinMode(umidsolo, INPUT);
  pinMode(nivelagua, INPUT);
  pinMode(lampada, OUTPUT);
  pinMode(leds,OUTPUT);
  barramento.begin();
  barramento.getAddress(sensor, 0);  
}
void loop(){
  valorlum = analogRead(lum);
  valorumidar = analogRead(umidar);
  valorumidsolo = analogRead(umidsolo);
  nivelagua = analogRead(agua);
  valorpoten = analogRead(poten);
  cmd = sensorToLed(valorpoten);
  analogWrite(leds,cmd);
  Serial.print("Luminosidade: ");
  Serial.println(valorlum);
  Serial.print("Umidade do ar: ");
  Serial.println(valorumidar);
  Serial.print("Umidade do solo: ");
  Serial.println(valorumidsolo);
  Serial.print("Nível da água: ");
  Serial.println(nivelagua);
  barramento.requestTemperatures(); 
  float temperatura = barramento.getTempC(sensor);
  Serial.print("Temperatura: ");
  Serial.println(temperatura);
  digitalWrite(lampada, HIGH);
  delay(500);
  digitalWrite(lampada, LOW);
  delay(500);
}

int sensorToLed(int raw){
  int val = map(valorpoten, MIN_RAW, MAX_RAW, MIN_CMD, MAX_CMD);
  val=max(val,MIN_CMD);
  val=min(val,MAX_CMD);
  return val;
}