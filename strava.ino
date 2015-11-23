 
 /// GLOBALS ///////////////////////////////////////

int incomingByte = 0;  
const int motorPinOne = 2;
const int motorPinTwo = 3;

void setup() {
		
		Serial.begin(9600);     
		// opens serial port, sets data rate to 9600 bps
		pinMode(motorPinOne,OUTPUT);
        pinMode(motorPinTwo,OUTPUT);
        digitalWrite(motorPinOne, LOW);
        digitalWrite(motorPinTwo, LOW);
}

void loop() {

	

	if (Serial.available() > 0) {
		

	  	// read the incoming byte:
	  	incomingByte = Serial.read();
	    Serial.print("I received: ");
	    Serial.println(incomingByte, DEC);

	    if (incomingByte == 0) {
	    	digitalWrite(motorPinOne, HIGH);
	    	delay(50);
	    	digitalWrite(motorPinOne, LOW);
	    }
	    
	    if (incomingByte == 1) {
	    	digitalWrite(motorPinTwo, HIGH);
	    	delay(50);
	    	digitalWrite(motorPinTwo, LOW);
	    }
	}
	

}


/*
currentMillis = millis();
	if (motor1state == LOW) {
		if(currentMillis - previousMotorMillis >= motorInterval){
			motor1state == HIGH;
			digitalWrite(motorPinOne, motor1state);
			previousMotorMillis = motorInterval;
		}
	} else {
		if (currentMillis - previousMotorMillis >= motorInterval) {
			motor1state = LOW;
			digitalWrite(motorPinOne, motor1state);
			previousMotorMillis = motorInterval;
		}
	}
*/