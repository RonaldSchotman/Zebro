// 
// 
// 

#include "MotorController.h"

MotorController::MotorController()
{
	Serial.println("constructor called");	
	InitLegs();
	PersonalSettings();
	StartUp();
}

MotorController::~MotorController()
{
}

void MotorController::InitLegs()
{
	pinMode(EN1, OUTPUT);
	digitalWrite(EN1, LOW);
	pinMode(PWM_LF, OUTPUT);
	pinMode(DIR_LF, OUTPUT);
	pinMode(HALL_LF, INPUT_PULLUP);
	pinMode(PWM_LM, OUTPUT);
	pinMode(DIR_LM, OUTPUT);
	pinMode(HALL_LM, INPUT_PULLUP);
	pinMode(PWM_LA, OUTPUT);
	pinMode(DIR_LA, OUTPUT);
	pinMode(HALL_LA, INPUT_PULLUP);
	pinMode(PWM_RF, OUTPUT);
	pinMode(DIR_RF, OUTPUT);
	pinMode(HALL_RF, INPUT_PULLUP);
	pinMode(PWM_RM, OUTPUT);
	pinMode(DIR_RM, OUTPUT);
	pinMode(HALL_RM, INPUT_PULLUP);
	pinMode(PWM_RA, OUTPUT);
	pinMode(DIR_RA, OUTPUT);
	pinMode(HALL_RA, INPUT_PULLUP);
	legs[0] = new LegModule(new MoterModule(PWM_LF, DIR_LF, EN1), HALL_LF);
	legs[1] = new LegModule(new MoterModule(PWM_LM, DIR_LM, EN1), HALL_LM);
	legs[2] = new LegModule(new MoterModule(PWM_LA, DIR_LA, EN1), HALL_LA);
	legs[3] = new LegModule(new MoterModule(PWM_RF, DIR_RF, EN1), HALL_RF);
	legs[4] = new LegModule(new MoterModule(PWM_RM, DIR_RM, EN1), HALL_RM);
	legs[5] = new LegModule(new MoterModule(PWM_RA, DIR_RA, EN1), HALL_RA);
	group1[0] = legs[0], group1[1] = legs[2], group1[2] = legs[4];
	group2[0] = legs[1], group2[1] = legs[3], group2[2] = legs[5];
	Serial.println("init finished");
}

void MotorController::PersonalSettings()
{
	legs[0]->moter->SetDirection(0);
	legs[1]->moter->SetDirection(0);
	legs[2]->moter->SetDirection(0);
	legs[3]->moter->SetDirection(1);
	legs[4]->moter->SetDirection(1);
	legs[5]->moter->SetDirection(1);
	Serial.println("dir set");
}


void MotorController::StartUp()
{
	for (uint8_t i = 0; i < 6; i++)
	{
		legs[i]->moter->Stop();
	}
	for (uint8_t i = 0; i < 6; i++)
	{
		legs[i]->Step();
		delay(200);
		while (digitalRead(legs[i]->hallSensorPin) == HIGH) {}

		legs[i]->moter->Stop();
		legs[i]->ready = true;
		delay(500);
	}
}

void MotorController::StandUp()
{
	
}


bool MotorController::LegsReady()
{
	for (uint8_t i = 0; i < NumLegs; i++)
	{
		if (!(legs[i]->ready))
		{
			return false;
		}
	}
	return true;
}

void MotorController::DefaultWalkForward()
{
	steps = 18446744073709551615;
	StepOne();
}

void MotorController::DefaultWalkForward(uint16_t numberOfSteps)
{
	this->steps = numberOfSteps;
	StepOne();
}

void MotorController::StepOne()
{
	if (this->steps > 0) {
		Serial.println("stepOne");
		uint8_t speed = 10;
		for (uint8_t i = 0; i < 3; i++)
		{
			group1[i]->Step();
		}
		speed = speed + 10;
		while (speed < 100) {
			for (uint8_t i = 0; i < 3; i++)
			{
				group2[i]->moter->SetSpeed(speed);
			}
		}
		for (uint8_t i = 0; i < 3; i++)
		{
			while (digitalRead(group1[i]->hallSensorPin) == LOW) {}
		}
		while (!LegsReady())
		{
			for (uint8_t i = 0; i < 3; i++)
			{
				if (digitalRead(group1[i]->hallSensorPin) == LOW)
				{
					group1[i]->moter->Stop();
					group1[i]->ready = true;
				}
			}
		}
		Serial.println("stepOne done");
		StepTwo();
	}
}

void MotorController::StepTwo()
{
	Serial.println("stepTwo");
	uint8_t speed = 10;
	for (uint8_t i = 0; i < 3; i++)
	{
		group2[i]->Step();
	}
	speed = speed + 10;
	while (speed < 100) {
		for (uint8_t i = 0; i < 3; i++)
		{
			group2[i]->moter->SetSpeed(speed);
		}
	}
	for (uint8_t i = 0; i < 3; i++)
	{
		while (digitalRead(group2[i]->hallSensorPin) == LOW) {}
	}
	while (!LegsReady())
	{
		for (uint8_t i = 0; i < 3; i++)
		{
			if (digitalRead(group2[i]->hallSensorPin) == LOW)
			{
				group2[i]->moter->Stop();
				group2[i]->ready = true;
			}
		}
	}
	Serial.println("stepTwo done");
	this->steps--;
	StepOne();
}