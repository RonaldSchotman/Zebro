#ifndef COMMUNICATIONS_H
#define COMMUNICATIONS_H

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

vector<unsigned int> rewriteTime(vector<float> Vec);

void SendToLeg(vector<float> Vec,double time,int adress);

vector<float> SendVecUpdater(vector <float> PrevVec,vector<float> CurVec,vector<float> NextVec,double time,vector<int> ard);

vector<float> SendVecUpdaterS(vector <float> PrevVec,vector<float> CurVec,vector<float> NextVec,double time,vector<int> ard);

vector<float> SendVecCalc(vector <float> PrevVec,vector<float> CurVec,vector<float> NextVec,double time,vector<int> ard);

vector <int>  connectLegs();

vector<int> readAngleState(int adress, int pos);

vector<int> LegCheck(vector<float> CurVec, vector<float> NextVec,double time, vector<int> ard);

int SpecOps(int ch, vector<int> ard, uint8_t syncTime);

#endif
