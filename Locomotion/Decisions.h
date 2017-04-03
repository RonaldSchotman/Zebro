#ifndef DECISIONS_H
#define DECISIONS_H

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

// HEADER FILE FOR THE DECISION MAKER FUNCTION!! See .cpp file for more extensive explanations
vector<float> VecUpdater(vector<float> CurVec,vector<float> NextVec,double time); // Decides when it is time to change the current vector.

vector <float> CalcTau(int speed);	// Calculates the Tau-vector consisting of t_d (double stance time), t_f (flight time) and t_g (ground time) using the speed required by the Zebro

vector <float> CalcTauTest(int speed);	// Calculates the Tau-vector consisting of t_d (double stance time), t_f (flight time) and t_g (ground time) using the speed required by the Zebro

vector<vector<float> > gait(int speed); // This function calculates the Max-Plus gait matrix used depending on the speed required. 

#endif

