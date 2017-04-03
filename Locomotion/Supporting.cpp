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

// This file contains supporting files (e.g. files that are not necessarily important to change but are required for the operation of the program)
// It can be noted that there is some junk in this file. It may need some cleanup depending on which functions are used.


void printMatr(vector<vector<float> > A) // Prints a matrix
{
	int SizeM = A.size();
	for (int m = 0; m < (SizeM); ++m)
	{
		for (int n = 0; n< (SizeM); ++n)
		{
			cout << A[m][n] << "  ";
			if (n == (SizeM - 1))
				cout << "\n";
		}
	}
	cout << "\n";
}

void printVec(vector<float>A) // Prints a vector
{
	int SizeM = A.size();
	for (int m = 0; m < (SizeM); ++m)
	{
		cout << A[m] << "  ";
	}
	cout << "\n \n";
}

vector<float>MakeVector(float matr[], int size) // Turns an array into a vector
{
	vector<float> V(size, 0);			// Initializes the vector V with the size of the input *size*
	for (int n = 0; n < size; ++n)
	{
		V[n] = matr[n];					// Writes the i-th element of the vector V as the i-th element of the array *matr*
	}
	return V;							// Outputs V
}

vector<float> makeVec ( float Array[],int size) // Turns an array into a vector (again? yesh)
{
	vector<float> Vec (size,0);
	for (int i=0; i < size;++i)
	{
		Vec[i] = Array[i];
	}
	return Vec;
}



vector<float> NextV(vector<vector<float> > M, vector<float> V) // Calculates and prints the next timevector using V(k-1) and the Current gait
{
	vector <float> Vk = MPMVM(M, V);
	printVec(Vk);
	return Vk;
}

vector<float> Sim(vector<float> V) // Not used now.
{
	int speed;
	int speed2;
	int time;
	int sec;
	cout << "Please enter the desired speed value of the Zebro: ";
	cin >> speed;
	cout << "Please enter the desired time the speed value of the Zebro changes: ";
	cin >> time;
	cout << "Please enter the desired speed value after this change: ";
	cin >> speed2;
	cout << "Now enter the desired runtime of the simulation: ";
	cin >> sec;
	int deltat = 100;
	cout << "The value you entered is " << speed << ".\nThe robot will now start moving. \n";
	vector<int> V1(5,0);
	V1[0] = speed;
	V1[1] = sec;
	V1[2] = deltat;
	V1[4] = speed2;
	V1[3] = time;
	vector<int>SimVec = V1;
	vector<vector<float> > M = gait(SimVec[0]);
	// vector<float> V(12, 0);
	vector<float> Vnext = MPMVM(M, V);
	printVec(V);
	for (int n = 0; n < sec * 1000 / deltat; ++n)
	{
		if (n*0.1 >= MaxVec(V) || n*0.1 >= (MinVec(Vnext) - 0.5))
		{
			cout << "\r" << n*0.1 << "       ";
			cout << "\n";
			V = NextV(M, V);
			Vnext = MPMVM(M, V);
		}
		cout << "\r" << n*0.1 + 0.1 << "        ";
		if (n == SimVec[3] * 1000 / deltat)
		{
			M = gait(SimVec[4]);
		}
	}
	return V;
}

vector<float> UpdateV (vector<float> Vec , vector<float>Stat, vector<float> prevStat,float T) // Not used
{
	float dt = 0.1; //Synchronization value
	for (int i = 0; i<6 ; ++i)
	{
		if (prevStat[i] != Stat[i])
		{
			if (Stat[i] == 1) // Means if the leg is IN the air
				Vec[i] = T;
			else if (Stat[i] == 0) // The leg is ON the ground
				Vec[i+6] = T;
				if (Vec[i+6]>Vec[i])
					Vec[i] = Vec[i+6]+dt;
		}
	}
	return Vec ;
}



vector<float> CalcVelDelay(vector<float> V,vector<float> NextV, vector<float> curPos,float T, int i) // Not used
{
	float pi = 3.14159;
	float angleLiftOff = pi/4;
	float angleTouchDown = 2*pi - pi/4; 
	float maxAngVel = 10;
	float deltaPos; float deltaT ; 
		if (V[i+6]>T && curPos[i]>=pi)
		{
			deltaPos = 2*pi - curPos[i] + angleLiftOff;
			deltaT = V[i+6] - T ; 
		}
		else if (T<V[i+6] && curPos[i]>=0 && curPos[i]<pi)
		{
			deltaPos = angleLiftOff - curPos[i];
			deltaT = V[i+6] - T ; 
		}
		else if (T>=V[i+6] && T<V[i])
		{
			deltaPos = angleTouchDown - curPos[i];
			deltaT   = V[i]- T;
		}
		else if (T>=V[i] && T<NextV[i+6] && curPos[i]>pi)
		{
			deltaPos = 2*pi - curPos[i] + angleLiftOff;
			deltaT = NextV[i+6] - T ; 
		}
		else if (T >= V[i] && T<NextV[i+6] && curPos[i]>=0 && curPos[i] <= pi)
		{
			deltaPos = angleLiftOff - curPos[i];
			deltaT = NextV[i+6] - T ; 
		}
	
		vector<float> AngVelDelay (2,0);
		AngVelDelay[0] = deltaPos/deltaT;
		if (AngVelDelay[0]> maxAngVel)
		{
			float deltaVel = AngVelDelay[0] - maxAngVel;
			float Delay = deltaPos / deltaVel; 
			AngVelDelay[0]= maxAngVel;
			AngVelDelay[1]= Delay;
		}
			
		
		return AngVelDelay;
}

void changemode(int dir) // Necessary for the reset of kbhit
{
  static struct termios oldt, newt;

  if ( dir == 1 )
  {
    tcgetattr( STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~( ICANON | ECHO );
    tcsetattr( STDIN_FILENO, TCSANOW, &newt);
  }
  else
    tcsetattr( STDIN_FILENO, TCSANOW, &oldt);
}

int kbhit (void) // This function registrates IF a key is hit
{
  struct timeval tv;
  fd_set rdfs;

  tv.tv_sec = 0;
  tv.tv_usec = 0;

  FD_ZERO(&rdfs);
  FD_SET (STDIN_FILENO, &rdfs);

  select(STDIN_FILENO+1, &rdfs, NULL, NULL, &tv);
  return FD_ISSET(STDIN_FILENO, &rdfs);

}

int int_floor(double x)  // This function floors a number, and changes the number from a double to an integer
{ 
    return (int)(x+100000) - 100000; 
}

