#ifndef MAXPLUSCALC_H
#define MAXPLUSCALC_H

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

// HEADER FILE FOR MAX PLUS OPERATIONS! See the .cpp file for the extended explanations
// Yes, this is where the Max-Plus magic happens. Can you smell the vibe of invincibility surrounding you right now? I sure as hell can't
// Shootout to all the Zebros in the galaxy

float maxvecfloat(vector<float> v); // Makes a vector of an array

double maxvec(vector<double> v); //This function calculates the maximum value of a vector, further used in the max-plus calculations for matrices and vectors

vector<double> mpmatrixvecmult(double matr[][12], vector<double> vect); // This function multiplies a matrix and a vector with Max-Plus algebra ( in the following order: Matrix (OTIMES) Vector = Vector ) using the maxvec function

float MaxVec(vector<float>A); // Calculates the maximum value of a vector

float MinVec(vector<float>A); // Calculates the maximum value of a vector

float MPVM(vector<float> A, vector<float> B); // Max Plus vector multiplication

vector<float> MPMVM(vector<vector<float> > A, vector<float> B); // Max Plus Matrix Vector Multiplication (works just for square matrices) 

vector<vector<float> > MPMA(vector<vector<float> >A, vector<vector<float> >B); // Calculates the Max-Plus matrix addition as -> A oplus B = C

vector<vector<float> > MPMM(vector<vector<float> >A, vector<vector<float> >B); // Calculates the Max-Plus matrix multiplication as -> A otimes B=C

vector<float> VAdd(vector<float> A, vector<float> B); // Max-Plus vector multiplication elementwise (or the standard vector addition)

#endif
