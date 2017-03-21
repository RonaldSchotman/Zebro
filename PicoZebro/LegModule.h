// LegModule.h

#ifndef _LEGMODULE_h
#define _LEGMODULE_h
#include "MoterModule.h"

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class LegModule
{
public:
	LegModule();
	LegModule(MoterModule *, uint8_t);
	virtual ~LegModule();

	MoterModule * moter;
	uint8_t hallSensorPin;

	void Step();
	void Wave();
	bool ready = true;
};

#endif

