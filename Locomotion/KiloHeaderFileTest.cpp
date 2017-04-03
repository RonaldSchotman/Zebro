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
	//Initialization
	vector<int> ard = connectLegs(); uint8_t writeTime;
	auto begin = clock();
	auto nu= clock();
	double time = 0; double oldtime=0;  uint8_t syncTime=0;vector<float> CheckVec(12,0); vector<float> SendHelpVec(3,0);
	vector<vector<float> >CurStat; vector<float> CurVec; vector<float> NextVec; vector<float> SendVec(12,0);vector<float> PrevVec; vector<float> MemVec;
	//cout << time << "\n" ;
	int speed= 75;int oldspeed=75;
	vector <vector <float> > mpm = gait(speed);
	float HelpVec[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
	vector<float>Vec = makeVec(HelpVec,12);
	PrevVec= Vec;
	CurVec = MPMVM(mpm,Vec);
	NextVec = MPMVM(mpm,CurVec);
	int timecounter=1; int loopWait =10; //ms
	//printVec(CurVec);
	int ch=0;
	vector<int> legCheck (6,0);
	int a =0; int walking = 0;vector<int> readout;int readout2;int readout3;
	// LOOP
	while (1==1){
		// Check for input
		ch =0;
		changemode(1);
 		 if (kbhit()!=0){
 		 ch = getchar();
 		}
		////////////////


		//Status
		nu = clock();
		oldtime = floor(time);
		time =((std::difftime(nu,begin)/1000)+ loopWait*timecounter)/1000;
		//gait updater
		if (ch ==49) {speed = 75;}if (ch==50){speed=50;};if(ch==51){speed=25;}
		if (speed!=oldspeed){mpm=gait(speed);oldspeed=speed;}
		//CurStat = ReadStatus(time);
		MemVec = CurVec;
		//CurVec  = DelayCalc(CurVec,CurStat,time);
		CurVec  = VecUpdater(CurVec,NextVec,time);
		if (MemVec!=CurVec){PrevVec = MemVec;}
		NextVec =  MPMVM(mpm,CurVec);
		//Send
		if (floor(time)!=oldtime){
		syncTime = (uint8_t)floor(time) % 256;
		wiringPiI2CWriteReg8 (ard[6], 11, syncTime) ;
		readout = readAngleState(ard[3],1);
		/*
		readout = wiringPiI2CReadReg8 (ard[1], 110) ; // 110 111 angles, 112 direction (1,0) , 113 (finitestatemachine flag )
*/
		readout2= wiringPiI2CReadReg8 (ard[3], 111) ;
		readout3= wiringPiI2CReadReg8 (ard[3], 113) ;

		a = int(syncTime);
		cout <<"\n" <<  a<< "    "  << readout[0] <<"    " <<  readout2 << "    " <<readout3;
		}

		if ((ch == 119|| walking ==1))
                {
                        CheckVec= SendVecCalc(PrevVec,CurVec,NextVec,time,ard);
			if (CheckVec!=SendVec)
			{
				// Feedback
				legCheck = LegCheck(CurVec, NextVec,time, ard);
				// Actual Sending
				SendVec = SendVecUpdater(PrevVec,CurVec,NextVec,time,ard);cout<<"      Walking";
			}
                        walking =1;
                }
		//printVec(CurVec);
		//printVec(SendVec);
		//cout << ard[0];
		if (ch ==99)
		{
			// Calibrate
			wiringPiI2CWriteReg8(ard[6],30,1);
			wiringPiI2CWriteReg8(ard[6],37,1);
			cout<<  "         Calibrate";
		}
		if (ch ==122)
		{
			// Standup
			 // [0] = tlb (sec), [1] = ttb (sec), [2] = tla (ms/4), [3] = tta (ms/4)
			writeTime = (uint8_t) syncTime;
	       		uint8_t Data[8] = {2,0,(uint8_t) (writeTime+3),0,0,1,0,1};
        		for (uint8_t i=0;i<9;i++)
        		{
        			wiringPiI2CWriteReg8(ard[6],30+i,Data[i]);
        			delayMicroseconds(1);
       			 }

			cout<<  "         Stand Up";
		}
		if (ch ==101)
		{
		        // Reset Emergency Stop
 		       wiringPiI2CWriteReg8 (ard[6], 22, 0x12) ;
			cout<<  "         Reset Emergency Stop";

		}
		if (ch == 32)
		{
			// Stop Moving
			wiringPiI2CWriteReg8 (ard[6], 30, 255) ;
			wiringPiI2CWriteReg8 (ard[6], 37, 1) ;
			walking =0;
			cout<< "       PANIC STOP"  ;
		}
		if (ch == 114)
                {
                        // Go back to the idle state
                        wiringPiI2CWriteReg8 (ard[6], 30, 0) ;
                        wiringPiI2CWriteReg8 (ard[6], 37, 1) ;
                        walking =0;
                        cout<< "       RESET"  ;
                }

		changemode(0);delay(loopWait);timecounter++;
	}




}
