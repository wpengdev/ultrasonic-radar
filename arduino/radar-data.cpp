#include <Servo.h>
#include <HCSR04.h>

//Define pins
const int servopin = 9;
const int potpin = A0; //A0 is same as 14
const int trigpin = 10;
const int echopin = 11;

//Create servo object
Servo myServo;
//Create sensor object
HCSR04 goggles(trigpin, echopin);

void setup() {
  
  //Tells servo which pin to receive signals from
  myServo.attach(servopin);

  //Don't need to establish pin modes as library handles it for servo and potentiometer

  //Initialise sensor
  goggles.begin();

  //Initialise serial
  Serial.begin(9600);
  //Serial.println("Starting up RADAR -------------------------");
}

void loop() {

  //Receives analog data from potentiometer
  int potnum = analogRead(potpin);

  //Maps analog data to angle
  int servoangle = map(potnum, 0, 1023, 0, 180);

  //Writes angle to servo
  myServo.write(servoangle);

  //Store distance
  float dist = goggles.getDistanceCM();
  //Serial.print("Distance: ");
  Serial.print(servoangle);
  Serial.print(",");
  Serial.println(dist);
  //Serial.print("cm | Angle: ");
  
  delay(15);
}
