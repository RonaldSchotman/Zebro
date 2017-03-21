//
//
//

#include "MoterModule.h"


MoterModule::MoterModule(uint8_t PwmPin, uint8_t DirectionPin, uint8_t EnablePin): pwmPin(PwmPin), directionPin(DirectionPin), enablePin(EnablePin)
{
	pinMode(pwmPin, OUTPUT);
	pinMode(directionPin, OUTPUT);
	pinMode(enablePin, OUTPUT);

	//ToDo: attach interrupt to faultPin signal.
	//Or not, faultpin does not exist on the actual pico zebro
	//attachInterrupt(faultPin, stopeverything, LOW);
}

MoterModule::~MoterModule()
{
}

void MoterModule::Stop() const
{
	digitalWrite(this->pwmPin, 0);
}

void MoterModule::SetDirection(uint8_t DIRECTION) const
{
	digitalWrite(directionPin, DIRECTION);
}

void MoterModule::SetSpeed(uint8_t SPEED) const
{
	analogWrite(this->pwmPin, SPEED);
}