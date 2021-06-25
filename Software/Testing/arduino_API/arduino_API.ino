//----------------------------------------------------------------------------------
// This script applies a way for a python script to send data through the arduino file and through the CAN bus interface, thus allowing data sending and recieving in a single python package.
//----------------------------------------------------------------------------------

// Include all the canbus necessary libraries
#include <Canbus.h>
#include <defaults.h>
#include <global.h>
#include <mcp2515.h>
#include <mcp2515_defs.h>

int ledPin1 = 7;
int ledPin2 = 8;
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
    setALL(command);
    Serial.println("LED ON");
  }
  else if (command == "off") {
    setALL(command);
    Serial.println("LED OFF");
  }

  // Handle the string data that has the rfid number
  String rfidStr = getValue(command,',',1);
  int rfidNum = rfidStr.toInt();
  switch (rfidNum) {
    case 1:
      resetLED(ledPin1, rfidStr);
      break;
    case 2: 
      resetLED(ledPin2, rfidStr);
      break;
    case 3:
      resetLED(ledPin3, rfidStr);
      break;
    case 4:
      resetLED(ledPin4, rfidStr);
      break;
    default:
      break;
  }
}

void resetLED(int pin, String ref) {
  // This function blinks the LED at the given pin for the given time
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(ledPin4, LOW);

  digitalWrite(pin, HIGH);
  Serial.println("Passed" + ref);
}

void setALL(String command) {
  // This function sets all the LEDS to the specified state
  if (command == "on") {
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin4, HIGH);
  }
  else if (command == "off") {
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin4, LOW);
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
