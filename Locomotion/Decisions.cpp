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

//In this file, the functions for the decision maker are used. This makes sure that the correct gait, flight times and ground times are chosen 
vector<float> VecUpdater(vector<float> CurVec,vector<float> NextVec,double time)
{
	vector<float> Vec(12,0);
	float max = maxvecfloat(CurVec);
	double maxdub = double(max);
	if(maxdub<time)
	{
		Vec = NextVec;
	}
	else 
	{ 
		Vec = CurVec;
	}
	return Vec;
}

vector <float> CalcTau(int speed)	// Calculates the Tau-vector consisting of t_d (double stance time), t_f (flight time) and t_g (ground time) using the speed required by the Zebro
{									// Approx. of the 6-step time (the time it takes for all legs to rotate) of the Zebro: 
	// T_barGCC = CrawlingCat(max(6td+5tf,tg)  , T_barGTS = TwoStep(3td+2tf,tg), T_barGTG = TripodGait(2td+tf,tg)
	// For optimal transitions, the speeds of the Zebro need to as close as possible to each other
	// NEEDS A LOT OF WORK M8

	float mintd = 0.25;			 float destd = 0.5;				float maxtd = 1;			 // Defines the minimal, desired and maximal double stance time 
	float mintf = 0.5;			 float destf = 1;				float maxtf = 2;			 // Defines the minimal, desired and maximal flight time 
	float mintg = mintd + mintf; float destg = destd + destf;  float maxtg = maxtd + maxtf; // Defines the minimal, desired and maximal flight time
	float td = destd; float tf = destf; float tg = destg;
	if (speed <= 40)
	{
		td = maxtd - 0.75*speed;
		tf = 2 * td;
		tg = tf + td;
	}
	if (speed > 40 && speed <= 70)
	{
		float T_bar = 6 * mintd + 5 * mintf;
		td = T_bar / (7) - (speed - 40) / (70 - 40)*(T_bar / 7 - 0.25);
		tf = 2 * td;
		tg = tf + td;
	}
	if (speed > 70)
	{
		if (speed > 100)
			speed = 100;
		td = (3 * mintd + 2 * mintf) / (4) - (speed - 70) / (100 - 70);
		tf = 2 * td;
		tg = td + tf+ 0*(mintg+maxtg);
	}
	 
	float Tauarr[3] = { td, tf, tg };				// Write the Tau in an array
	vector<float> Tau = MakeVector(Tauarr, 3);		// Uses the MakeVector function to define Tau as a vector
	return Tau;										// Returns Tau
}


vector <float> CalcTauTest(int speed)	// Calculates the Tau-vector consisting of t_d (double stance time), t_f (flight time) and t_g (ground time) using the speed required by the Zebro
{									// Approx. of the 6-step time (the time it takes for all legs to rotate) of the Zebro: 
	// T_barGCC = CrawlingCat(max(6td+5tf,tg)  , T_barGTS = TwoStep(3td+2tf,tg), T_barGTG = TripodGait(2td+tf,tg)
	// For optimal transitions, the speeds of the Zebro need to as close as possible to each other

	float mintd = 0.25;			 float destd = 0.0;				float maxtd = 1;			 // Defines the minimal, desired and maximal double stance time 
	float mintf = 0.5;			 float destf = 1.0;				float maxtf = 2;			 // Defines the minimal, desired and maximal flight time 
	float mintg = mintd + mintf;		 float destg = destd + destf;  			float maxtg = maxtd + maxtf; // Defines the minimal, desired and maximal flight time
	float td = destd; float tf = destf; float tg = destg;
	int ulCC = 33; int ulTS = 67; int ulTP = 100;
	if (speed <= ulCC)
	{
		td = destd;
		tf = destf;
		tg = destg;
	}
	if (speed > ulCC && speed <= ulTS)
	{
		td = destd;
		tf = destf;
		tg = destg;
	}
	if (speed > ulTS && speed <= ulTP)
	{
		td = destd;
		tf = destf;
		tg = destg+(mintg+maxtg)*0;
	}

	float Tauarr[3] = { td, tf, tg };				// Write the Tau in an array
	vector<float> Tau = MakeVector(Tauarr, 3);		// Uses the MakeVector function to define Tau as a vector
	return Tau;										// Returns Tau
}


//-----------------------------------------------------------------------------------------------------------------------------
// The gait determination function
vector<vector<float> > gait(int speed) // This function calculates the Max-Plus gait matrix used depending on the speed required. 
{
	vector<float> Tau = CalcTauTest(speed);	// Calculates the Tau-vector which contains the t_f (flight time), the t_d (double stance time) and the t_g (ground time)
	vector<vector<float> > P;			// Initialize vector P
	vector<vector<float> > Q;			// Initialize vector Q


	if (speed == 1)
	{
		P = CornerLeftP(Tau);
		Q = CornerLeftQ(Tau);
	}
	if (speed == 2)
	{
		P = CornerLeftP(Tau);
		Q = CornerLeftQ(Tau);
	}
	if (speed > 67)
	{
		P = TripodP(Tau);				// Define the P-matrix as the matrix used to calculate the Tripod Gait (1,4,5)->(2,3,6)
		Q = TripodQ(Tau);				// Define the P-matrix as the matrix used to calculate the Tripod Gait (1,4,5)->(2,3,6)
	}
	else if (speed > 33 && speed <= 67)
	{
		P = TwoStepP(Tau);				// Define the P-matrix as the matrix used to calculate the TwoStep Gait (1,4)->(3,6)->(5,2)
		Q = TwoStepQ(Tau);				// Define the Q-matrix as the matrix used to calculate the TwoStep Gait (1,4)->(3,6)->(5,2)
	}
	else if (speed <= 33)
	{
		P = CrawlingCatP(Tau);			// Define the P-matrix as the matrix used to calculate the Crawling Cat Gait (1)->(2)->(3)->(4)->(5)->(6)
		Q = CrawlingCatQ(Tau);			// Define the Q-matrix as the matrix used to calculate the Crawling Cat Gait (1)->(2)->(3)->(4)->(5)->(6)
	}

	vector < vector<float> > A0 = A0Matr(Tau, P);			// Calculates the A_0 matrix using the Tau-vector and the P-matrix
	vector < vector<float> > A1 = A1Matr(Tau, Q);			// Calculates the A_1 matrix using the Tau-vector and the Q-matrix
	vector < vector<float> > A0star = KleeneStarOp(A0);		// Calculates A_0* using the A_0 matrix following the Kleene Star operation
	vector < vector<float> > chosenGait = MPMM(A0star, A1);  	// Calculates the Max-Plus gait matrix using A_0* and A_1
	return chosenGait;
}


//-----------------------------------------------------------------------------------------------------------------------------
// Defines gait according to input
int GaitChangeManual (int ch)
{ 
	int speeds;	
	if (ch ==49){speeds = 75;}if (ch==50){speeds=50;};if(ch==51){speeds=25;} // Changes gaits with buttons 1,2,3
	if (ch==111){speeds=1;};if(ch==112){speeds=2;};if (ch==105){speeds=75;}   // Supposed to change between tripod, left and right
	return speeds;
}


