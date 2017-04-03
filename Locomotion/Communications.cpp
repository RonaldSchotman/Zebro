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

// THIS FILE IS FOR THE COMMUNICATION WITH THE KILO ZEBRO 
// The functions are made to have a working communications between the PI and Zebro. It can be noted that certain conversion functions are included.


//-----------------------------------------------------------------------------------------------------------------------------
// The time rewrite function (time -> Zebro Time)
vector<unsigned int> rewriteTime(vector<float> Vec) // Rewrites the time to make sure it can be passed on to the KILO
{
        unsigned int Tlb = floor(Vec[0]); //liftoff time in whole seconds
        unsigned int Ttb = floor(Vec[1]); //touchdown time in whole seconds
       // unsigned int Tla = floor(((time-Tlb)*1000)/4); // behind the comma
       // unsigned int Tta = floor(((time-Ttb)*1000)/4);// behind the comma
        unsigned int Tla = int(floor(((Vec[0]-Tlb)*1000)/4));
        unsigned int Tta = int(floor(((Vec[1]-Ttb)*1000)/4));
        vector<unsigned int> rewriteTime (4,0);
        rewriteTime[0] = Tlb;rewriteTime[1] = Ttb;rewriteTime[2] = Tla;rewriteTime[3] = Tta;
        return rewriteTime;
}
//-----------------------------------------------------------------------------------------------------------------------------
// Sends the liftoff and touchdown times to the seperate legs, as well as the operation modus. This is for forward walking
void SendToLeg(vector<float> Vec,double time,int adress)
{
	vector<unsigned int> TimeVec = rewriteTime(Vec); // [0] = tlb (sec), [1] = ttb (sec), [2] = tla (ms/4), [3] = tta (ms/4)
	uint8_t Data[8] = {3,(uint8_t) TimeVec[2],(uint8_t) TimeVec[0],(uint8_t) TimeVec[3],(uint8_t) TimeVec[1],1,0,1};
	for (uint8_t i=0;i<9;i++)
	{
	wiringPiI2CWriteReg8(adress,30+i,Data[i]);
	delayMicroseconds(1);
	}
}
//-----------------------------------------------------------------------------------------------------------------------------
// Calculates the lift off and touchdown data that needs to be send, and sends it.
vector<float> SendVecUpdater(vector <float> PrevVec,vector<float> CurVec,vector<float> NextVec,double time,vector<int> ard)
{
	vector<float> Vec(3,0);
	vector<float> OutPutVec(12,0);
	for (int i=0;i<6;i++)
	{
		Vec[0] =0;Vec[1]=0;Vec[2]=0;
		if (time<CurVec[i+6])
		{
			Vec[0] = CurVec[i+6]; Vec[1] = CurVec[i]; Vec[2]=3; // Vec[0] = liftoff, Vec[1] = touchdown, Vec[2] = mode aperandi
		}
		else if (time<CurVec[i] && time>=CurVec[i+6])
		{
			Vec[0] = NextVec[i+6]; Vec[1] = CurVec[i]; Vec[2] = 3;
		}
		else if (time>=CurVec[i] &&  time<=NextVec[i+6])
		{
			Vec[0] = NextVec[i+6]; Vec[1]= NextVec[i]; Vec[2] = 3;
		}
		else
		{
			cout<< " Error in SendVecUpdater";
		}
		SendToLeg(Vec,time,ard[i]);
		OutPutVec[i] = Vec[0];
		OutPutVec[i+6]=Vec[1]; 
	}
	return OutPutVec;
}

//-----------------------------------------------------------------------------------------------------------------------------
// Calculates the lift off and touchdown data that needs to be send, but does not send it. This function is made to reduce the amount of sent instructions
vector<float> SendVecCalc(vector <float> PrevVec,vector<float> CurVec,vector<float> NextVec,double time,vector<int> ard)
{
        vector<float> Vec(3,0);
        vector<float> OutSendVec(12,0);
        for (int i=0;i<6;i++)
        {
                Vec[0] =0;Vec[1]=0;Vec[2]=0;
                if (time<CurVec[i+6])
                {
                        Vec[0] = CurVec[i+6]; Vec[1] = CurVec[i]; Vec[2]=3; // Vec[0] = liftoff, Vec[1] = touchdown, Vec[2] = mode aperandi
                }
                else if (time<CurVec[i] && time>=CurVec[i+6])
                {
                        Vec[0] = NextVec[i+6]; Vec[1] = CurVec[i]; Vec[2] = 3;
                }
                else if (time>=CurVec[i] &&  time<=NextVec[i+6])
                {
                        Vec[0] = NextVec[i+6]; Vec[1]= NextVec[i]; Vec[2] = 3;
                }
                else
                {
                        cout<< " Error in SendVecCalculator";
                }
                OutSendVec[i] = Vec[0]; 
                OutSendVec[i+6]=Vec[1]; 
        }
        return OutSendVec;
}
//-----------------------------------------------------------------------------------------------------------------------------
// Connects the legs to the right I2C adresses
vector <int>  connectLegs()  // Function to connect the legs to give the legs an adress that the PI can operate with
{
	wiringPiSetupGpio();
	vector<int> ard (7,0);
	ard[0] = wiringPiI2CSetup(0x10); // Left front leg
	ard[1] = wiringPiI2CSetup(0x16); // Right front leg
	ard[2] = wiringPiI2CSetup(0x12); // Left middle leg
	ard[3] = wiringPiI2CSetup(0x18); // Right middle leg
	ard[4] = wiringPiI2CSetup(0x14); // Left hind leg
	ard[5] = wiringPiI2CSetup(0x1a); // Right hind leg
	ard[6] = wiringPiI2CSetup(0x00); // Adress to send a command to all legs simultanuously
	return ard;
}
//-----------------------------------------------------------------------------------------------------------------------------
// Reads the angles to of the legs, and rewrites them in degrees (0 to 360)
vector<int> readAngleState(int adress, int pos) //1 = right , 0 = left
{
	int Angle1=wiringPiI2CReadReg8 (adress, 110) ; // Read angle (110 & 111)
	int Angle2=wiringPiI2CReadReg8 (adress, 111) ;
	int Dir =wiringPiI2CReadReg8 (adress, 112) ; // Read direction (112)
	int StepStat = wiringPiI2CReadReg8 (adress, 113) ; // Read current step
	int TotAngle = Angle2*256 + Angle1;
	if (pos == 1)					//       2pi/0 (360/0)
	{						//             |
		TotAngle = 910-TotAngle;		//1/2*pi(90)---|-----3/2*pi (270)
	}						//	       |
	double CalcAngle =(double) TotAngle/910*360;    //	    pi(180)
	int CorAngle = (int) floor(CalcAngle);
	vector <int> Stat (3,0);
	Stat[0] = CorAngle; Stat[1] = Dir; Stat[2]= StepStat;
	return Stat;
}

//----------------------------------------------------------------------------------------------------------------------------
// This function checks if the legs are in the correct place. They should listen to what I say.
vector<int> LegCheck(vector<float> CurVec, vector<float> NextVec,double time, vector<int> ard)
{
	vector<int> curStat(6,0); int tda=140;int loa=95; int deltaa =10;
	vector<int> legStat(3,0);
	int pos=0;
	int bugCheck =0;
	for (int i=3;i<4;i++)
        {
		if (i%2==0){pos=0;}else{pos=1;}
		legStat = readAngleState(ard[i],pos);
                if (time<CurVec[i+6] &&  (legStat[0]<(tda+deltaa) || legStat[0]>(loa- deltaa)))
                {
                        curStat[i]=1;
			bugCheck =1;
			cout<< bugCheck;
                }
                else if (time<CurVec[i] && time>=CurVec[i+6]&& (legStat[0]>(tda-deltaa) && legStat[0]<(loa+deltaa)))
                {
                        curStat[i]=1;
			bugCheck =2;
			cout<< bugCheck;
                }
                else if (time>=CurVec[i] &&  time<=NextVec[i+6] && (legStat[0]<(tda+deltaa) || legStat[0]>(loa-deltaa)))
                {
                        curStat[i]=1;
			bugCheck =3;
			cout<< " Deze gaat goed:   " << bugCheck;
                }
                else
                {
                        curStat[i]=0; cout<<" Too slow or other error in leg   " << i << "     " << legStat[0] << "Curvec     " << CurVec[i];
                }
	}
	return curStat;
}




