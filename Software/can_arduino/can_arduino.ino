// Includes
#include <Canbus.h>
#include <defaults.h>
#include <global.h>
#include <mcp2515.h>
#include <mcp2515_defs.h>

// Variables
int buttonPin = 4;
int buttonState;
// Setup
void setup() {
  // Setup serial
  Serial.begin(9600);
  Serial.println("Simulation Start");

  // Setup pins
  pinMode(buttonPin, INPUT);
  
}

// Body
void loop() {
  // Right now just test the button functionality
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);
  delay(100);
}
