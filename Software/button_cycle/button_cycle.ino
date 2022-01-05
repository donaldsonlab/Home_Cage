// Variables
int buttonPin = 4;
int buttonState;
int prevState = LOW;

void setup() {
  // Setup serial
  Serial.begin(9600);
  Serial.println("Simulation Start");

  // Setup pins
  pinMode(buttonPin, INPUT);
}

void loop() {
  // Monitor the button
  buttonState = digitalRead(buttonPin);
//  Serial.println(buttonState);
//  delay(100);
  if ((buttonState == HIGH) && (prevState == HIGH)) {
    // IF the button is pressed, check the previous press as well
    Serial.println("ON");
  }
   else {
    Serial.println("OFF");
   }
   prevState = buttonState;
}
