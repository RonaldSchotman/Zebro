#ifndef GAITS_H
#define GAITS_H

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

// HEADER FILE FOR GAITS! See the .cpp file for the extended explanations

vector < vector<float> >CornerRightP(vector<float> A); // 

vector < vector<float> >CornerRightQ(vector<float> A); // 

vector < vector<float> >CornerLeftP(vector<float> A); // 

vector < vector<float> >CornerLeftQ(vector<float> A); // 

vector < vector<float> >CrawlingCatP(vector<float> A); // Defines the P-matrix of the Crawling Cat gait

vector < vector<float> >CrawlingCatQ(vector<float> A); // Defines the Q-matrix of the Crawling Cat gait 

vector < vector<float> >TwoStepP(vector<float> A);	// Defines the P-matrix of the TwoStep gait

vector < vector<float> >TwoStepQ(vector<float> A); // Defines the Q-matrix of the TwoStep gait 

vector < vector<float> >TripodP(vector<float> A); // Defines the P-matrix from the Tripod Gait

vector < vector<float> >TripodQ(vector<float> A); // Defines the Q-matrix from the Tripod Gait


vector < vector<float> >tEmatr(float t); // Calculates a 6x6 diagonal matrix with t on the diagonal and -1 on the rest of the matrix


vector < vector<float> >tEmatrvar(float t, int size); // Calculates a diagonal matrix with t on the diagonal and -1 on the rest of the matrix (with an input for size)


vector < vector<float> > A0Matr(vector<float> Tau, vector<vector<float> >P); // Calculates the A_0 Matrix using the supplied P-Matrix


vector < vector<float> > A1Matr(vector<float> Tau, vector<vector<float> >Q); // Calculates the A_1 Matrix using the supplied Q-Matrix


vector < vector<float> > KleeneStarOp(vector<vector<float> >A0); // The Kleene Star operation, which calculates: A_0* = sum(0->k) {A_0^k} (for calculation purposes uses k=10)


#endif
