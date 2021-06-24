//----------------------------------------------------------------------------------
// This script applies a way for a python script to send data through the arduino file and through the CAN bus interface, thus allowing data sending and recieving in a single python package.
//----------------------------------------------------------------------------------

// Include all the canbus necessary libraries
#include <Canbus.h>
#include <defaults.h>
#include <global.h>
#include <mcp2515.h>
#include <mcp2515_defs.h>

int ledPin1 = 10;
int ledPin2 = 11;
int ledPin3 = 12;
int ledPin4 = 13;
byte readChar;
String commData = "";

void setup() {
  // Initialize the serial monitor
  Serial.begin(9600);
  Serial.flush();

  // Initialize pins and set default values
  pinMode(ledPin1, OUTPUT);
  digitalWrite(ledPin1, LOW);
  pinMode(ledPin2, OUTPUT);
  digitalWrite(ledPin2, LOW);
  pinMode(ledPin3, OUTPUT);
  digitalWrite(ledPin3, LOW);
  pinMode(ledPin4, OUTPUT);
  digitalWrite(ledPin4, LOW);

  // Write starting message to the serial monitor
  Serial.println("Command Interpreter");
}

void loop() {
  // First, read the command in the serial monitor if there is one
  if (Serial.available()) {
    readChar = Serial.read(); // auto casts to byte type
    commData += (char)readChar; // compiles a full string of data

    if (readChar == '\r') {
      // The command is over
      commData.trim();
      commandHandle(commData);
      commData = ""; // re-initialize the command string
    } // \r
  } // available
}

void commandHandle(String command) {
  // This function handles the commands and sends each command to the correct function to execute
  if (command == "on") {
    // Turn the LED on
    digitalWrite(ledPin1, HIGH);
    Serial.println("LED ON");
  }
  else if (command == "off") {
    digitalWrite(ledPin1,LOW);
    Serial.println("LED OFF");
  }
  else {
    // Print back the command
    Serial.println("READ:" + command);
  }

  // Handle the string data that has the rfid number
  String rfidStr = getValue(command,',',1);
  int rfidNum = rfidStr.toInt();
  switch (rfidNum) {
    case 1:
      blinkLED(ledPin1,50);
      break;
    case 2: 
      blinkLED(ledPin2,50);
      break;
    case 3:
      blinkLED(ledPin3, 50);
      break;
    case 4:
      blinkLED(ledPin4, 50);
      break;
    default:
      break;
  }
}

void blinkLED(int pin, int stopTime) {
  // This function blinks the LED at the given pin for the given time
  digitalWrite(pin, HIGH);
  delay(stopTime);
  digitalWrite(pin, LOW);
}
