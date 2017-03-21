// MoterModule.h

#ifndef _MOTERMODULE_h
#define _MOTERMODULE_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class MoterModule
{
public:
	MoterModule(uint8_t PWM, uint8_t Direction, uint8_t EnablePin);
	virtual ~MoterModule();

	void Stop() const;
	void SetDirection(uint8_t) const;
	void SetSpeed(uint8_t) const;

private:
	uint8_t pwmPin;
	uint8_t directionPin;
	uint8_t enablePin;
};

#endif

