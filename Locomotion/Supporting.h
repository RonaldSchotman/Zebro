#ifndef SUPPORTING_H
#define SUPPORTING_H

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

// THIS IS THE HEADER FILE FOR SUPPORTING FUNCTIONS
// Take a look at the .cpp file for more information

void printMatr(vector<vector<float> > A);// Prints a matrix

void printVec(vector<float>A); // Prints a vector

vector<float>MakeVector(float matr[], int size); // Turns an array into a vector

vector<float> makeVec ( float Array[],int size); // Does the same

vector<float> UpdateV (vector<float> Vec , vector<float>Stat, vector<float> prevStat,float T); // Not used now


vector<float> Sim(vector<float> V); // Not used now.

vector<float> NextV(vector<vector<float> > M, vector<float> V); // Calculates and prints the next timevector using V(k-1) and the Current gait


vector<float> CalcVelDelay(vector<float> V,vector<float> NextV, vector<float> curPos,float T, int i); // Not used now


void changemode(int dir); // Necessary to reset the kbhit command


int kbhit (void); // Determines WHEN a key is pressed


int int_floor(double x) ; // FLoort dingen





#endif
