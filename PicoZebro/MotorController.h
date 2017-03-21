// MotorController.h

#ifndef _MOTORCONTROLLER_h
#define _MOTORCONTROLLER_h

#define PWM_LA 6
#define DIR_LA A6
#define HALL_LA A5

#define PWM_LM 7
#define DIR_LM A8
#define HALL_LM A7

#define PWM_LF 8
#define DIR_LF A9
#define HALL_LF A10

#define PWM_RA 46
#define DIR_RA 36
#define HALL_RA 37

#define PWM_RM 45
#define DIR_RM 34
#define HALL_RM 35

#define PWM_RF 44
#define DIR_RF 33
#define HALL_RF 32

#define EN1 30
#define NumLegs 6

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#include "LegModule.h"

class MotorController
{
public:
	MotorController();
	virtual ~MotorController();

	void InitLegs();
	void StartUp();
	void StandUp();
	void PersonalSettings();
	void DefaultWalkForward();
	void DefaultWalkForward(uint16_t);
	void StepOne();
	void StepTwo();

	bool LegsReady();
private:
	LegModule * legs[NumLegs];
	LegModule * group1[NumLegs / 2];
	LegModule * group2[NumLegs / 2];
	uint64_t steps = 0;
};

#endif

