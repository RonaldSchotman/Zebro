#include <iostream>
#include <sys/types.h>
#include <sys/time.h>
#include <vector>
#include <wiringPi.h>
#include <time.h>
#include <ctime>
#include <chrono>
#include <thread>
#include <wiringPiI2C.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <ncurses.h> 
#include <termios.h>
#include <fcntl.h>
#include "MaxPlusCalc.h"
#include "Gaits.h"
#include "Decisions.h"
#include "Supporting.h"
#include "Communications.h"
using namespace std;




int main()
{
	// Asks the operator for a starting speed
	int i;
  	cout << "Please enter a starting speed between 5-99: "; // Prints the question
  	cin >> i;						// Asks input
	cout << "Starting with speed" << i;

	// Establish connection to the legs
	vector<int> ard = connectLegs();  // Connects the legs using the I2C adresses defined. Ard contains the adresses
	
	// Initialisation of variables	
	double checktime=0; double time = 0; double oldtime=0;  uint8_t syncTime=0;vector<float> CheckVec(12,0); vector<float> SendHelpVec(3,0); 
	vector<vector<float> >CurStat; vector<float> CurVec; vector<float> NextVec; vector<float> SendVec(12,0);vector<float> PrevVec; vector<float> MemVec; float HelpVec[12] = {0,0,0,0,0,0,0,0,0,0,0,0};vector<float>Vec = makeVec(HelpVec,12);
	int ch=0;  int walking = 0;vector<int> readout;vector<int> legCheck (6,0); int VecChange=0;
	//int a =0;int readout2;int readout3;int uploadcounter=0; int turningleft=0;int turningright=0; int turningcounter=0;

	// Start the time 	
	auto begin = clock();   		// Defines the starting time of the program
	auto nu= clock();     			// Defines the current time
	int timecounter=1; int loopWait =10; 	// Counts the loops and defines the waiting time in loop to not overflow the I2C-bus	

	// Begin the initialisation of speed and gaits
	int speed= i;int oldspeed=i; 						// Initializes the current speed en starting speed
	vector <vector <float> > mpm = gait(speed);  				// Calculates the first gait
	PrevVec= Vec; CurVec = MPMVM(mpm,Vec); NextVec = MPMVM(mpm,CurVec); 	// Defines the first 3 touchdown/liftoff vectors

	
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////LOOPIE///////////////////////////////////////////////////////////////////////
	///////////////////////////////// Starts the walking LOOP! ////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  // LOOP // LOOP  //
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	while (1==1)
	{
		
		// Check for input
		ch =0; 			// Resets the character that is being (inputted (?))
		changemode(1);		// Necessary to record the keyboard hit
 		 if (kbhit()!=0) // Checks if there was a keyboard hit
		{	
 		 ch = getchar();	// Gets the character
 		}


		// Looking at the clock and synchronizing the time
		nu = clock();								// Defines the current moment
		oldtime = floor(time);							// Updates the old time
		checktime = time;							// Makes an old time not floored. 
		time =((std::difftime(nu,begin)/1000)+ (loopWait)*(timecounter))/1000;  // Calculates the in-program time
		if (floor(time)!=oldtime)
		{
			cout<< floor(time)<< "\n" ;
			if (walking==1){cout<<"Walking";}
			syncTime = (uint8_t)floor(time) % 256;				// Calculates the synctime (8-bit)
			wiringPiI2CWriteReg8 (ard[6], 11, syncTime) ;			// Sends the synctime to the leg
			// readout = wiringPiI2CReadReg8 (ard[1], 110) ; // 110 111 angles, 112 direction (1,0) , 113 (finitestatemachine flag )
		}


		// Special Input Operations (Stand-Up/Freeze/Stop/TRANSFORM INTO FIGHTING ROBOT)
		if (ch!=0)
		{
			walking = SpecOps(ch, ard, syncTime);
		}

		// Gait updater
		speed = GaitChangeManual(ch);				// Changes gait if the input is a certain character
		if (speed!=oldspeed)
		{mpm=gait(speed);oldspeed=speed;}	// Calculates the new gait matrix 
		
		// Lift-off/Touchdown Vector updater
		MemVec = CurVec; CurVec  = VecUpdater(CurVec,NextVec,time); // Checks whether a new LO/TD vector is necessary, and updates the CurVec if so.
		if (MemVec!=CurVec)
		{
			VecChange=1;
			PrevVec = MemVec;NextVec =  MPMVM(mpm,CurVec);	    // Calculates the new previous and next vectors
		}


		if ((ch == 119|| walking ==1))
                {
				for (int i=0;i<6;i++)
				{ 
					if ((time>=CurVec[i+6] && checktime<=CurVec[i+6])||(time>=CurVec[i] && checktime<=CurVec[i]))
					{
						VecChange=1;
					}
				}
				if (VecChange==1)
				{
                                	SendVec = SendVecUpdaterS(PrevVec,CurVec,NextVec,time,ard);
				}
                        	walking =1;
                }

		changemode(0);timecounter++;VecChange=0;delay(loopWait);
	}
	



}
