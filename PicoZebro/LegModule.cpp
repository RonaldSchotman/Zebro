// 
// 
// 

#include "LegModule.h"

LegModule::LegModule(MoterModule * Moter, uint8_t HallSensorPin) : moter(Moter), hallSensorPin(HallSensorPin)
{
	pinMode(hallSensorPin, INPUT_PULLUP);
}

LegModule::~LegModule()
{
}

void LegModule::Step()
{
	this->ready = false;
	this->moter->SetSpeed(120);
}

void LegModule::Wave()
{
	//ToDo: code to make the leg wave.
	//throw "Not yet implemented Exception";
}