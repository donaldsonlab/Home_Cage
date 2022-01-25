// Includes
#include <Canbus.h>
#include <defaults.h>
#include <global.h>
#include <mcp2515.h>
#include <mcp2515_defs.h>

// Variables
int buttonPin = 4;
int buttonState;
tCAN message;

// Setup
void setup() {
  // Setup serial
  Serial.begin(9600);
  Serial.println("Simulation Start");

  // Setup pins
  pinMode(buttonPin, INPUT);

  // Setup CAN
  if(Canbus.init(CANSPEED_500))  //Initialise MCP2515 CAN controller at the specified speed
    Serial.println("CAN Init ok");
  else
    Serial.println("Can't init CAN");

  // Give time to process
  delay(50);
}

// Body
void loop() {
  // Right now just test the button functionality
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    // Create and send the data to the pi FOR NOW JUST PRINT IT TO THE SCREEN
    Serial.println("Button Pushed");
    tCAN messageData = create_data();
    send_data(messageData); // Send it
  }
}

// Send Data Script
void send_data(tCAN message) {
  // Format and send the message
  // INPUTS: message (string) - the data string that will be sent to the raspberry pi
  Serial.println("Sending...");
  mcp2515_bit_modify(CANCTRL, (1<<REQOP2)|(1<<REQOP1)|(1<<REQOP0), 0);
  Serial.println("Modified");
  mcp2515_send_message(&message);

  // Find a way to print it???
  Serial.println("Sent"); // Most likely this should be in the form of a software serial

  // Delay for button push to not repeat
  delay(500);
}

// Create Data Function
tCAN create_data() {
  // Initially this function starts out with no input, but eventually will need to input the data and info that the arduino will send in the form of a can bus message.
  // INPUTS: voleId (string) - ID tag of the vole
  //         rfidId (string) - Rfid reader number
  Serial.println("Creating...");

  tCAN message;
  message.id = 0x631; // HEX formatted message ID
  message.header.rtr = 0;
  message.header.length = 8; // Message length

  // Vole Tag
  message.data[0] = 0x00;
	message.data[1] = 0x00;
	message.data[2] = 0x00;
	message.data[3] = 0x00; //formatted in HEX
	message.data[4] = 0x00;
	message.data[5] = 0x00;

  // RFID ID
	//message.data[6] = 0x30;
	//message.data[7] = 0x33; 
  Serial.println("Message Created");
  return message;
}
