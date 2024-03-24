int ledPin = 13;  // Define LED pin
boolean lightOn = false;  // Track LED state
unsigned long startTime = 0;  // Variable to store the start time

void setup() {
  pinMode(ledPin, OUTPUT);  // Set LED pin as output
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();  // Read incoming data
    if (signal == '1') {  // Check if received signal is '1'
      lightOn = true;  // Turn on LED
      startTime = millis();  // Record the start time
    }
  }

  // Check if LED should be on or off
  if (lightOn) {
    digitalWrite(ledPin, HIGH);  // Turn on LED
  } else {
    digitalWrite(ledPin, LOW);  // Turn off LED
  }

  // Check if 10 seconds have elapsed and turn off the LED
  if (lightOn && millis() - startTime >= 7000) {  // 10000 milliseconds = 10 seconds
    lightOn = false;
  }
}
