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

// In this file, the different P and Q submatrices can be seen, as well as the files necessary to create the gait matrices. 

//------------------------------------------------------------------------------------------------------
// 1 leg at the time following the rithm 1-2-3-4-5-6 WAVE123456

vector < vector<float> >CrawlingCatP(vector<float> A) // Defines the P-matrix of the Crawling Cat gait
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { td, -1, -1, -1, -1, -1 }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { -1, td, -1, -1, -1, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, -1, td, -1, -1, -1 }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, -1, -1, td, -1, -1 }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { -1, -1, -1, -1, td, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}

vector < vector<float> >CrawlingCatQ(vector<float> A) // Defines the Q-matrix of the Crawling Cat gait 
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, -1, -1, -1, -1, td }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}

//------------------------------------------------------------------------------------------------------
// 2 legs at the time following the rithm 1,4 - 3,6 - 5,2 TWOSTEP14

vector < vector<float> >TwoStepP(vector<float> A)	// Defines the P-matrix of the TwoStep gait
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { -1, -1, td, -1, -1, td }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { td, -1, -1, td, -1, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, -1, td, -1, -1, td }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { td, -1, -1, td, -1, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}

vector < vector<float> >TwoStepQ(vector<float> A) // Defines the Q-matrix of the TwoStep gait 
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, td, -1, -1, td, -1 }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, td, -1, -1, td, -1 }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}

//------------------------------------------------------------------------------------------------------
// 3 legs at the time following the rithm 1,4,5 - 2,3,6  TRIPOD145

vector < vector<float> >TripodP(vector<float> A) // Defines the P-matrix from the Tripod Gait
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { td, -1, -1, td, td, -1 }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { td, -1, -1, td, td, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { td, -1, -1, td, td, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}

vector < vector<float> >TripodQ(vector<float> A) // Defines the Q-matrix from the Tripod Gait
{
	float td = A[0];
	vector<vector<float> > P(6, vector<float>(6));
	float P1arr[6] = { -1, td, td, -1, -1, td }; vector<float> P1 = MakeVector(P1arr, 6);
	float P2arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P2 = MakeVector(P2arr, 6);
	float P3arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P3 = MakeVector(P3arr, 6);
	float P4arr[6] = { -1, td, td, -1, -1, td }; vector<float> P4 = MakeVector(P4arr, 6);
	float P5arr[6] = { -1, td, td, -1, -1, td }; vector<float> P5 = MakeVector(P5arr, 6);
	float P6arr[6] = { -1, -1, -1, -1, -1, -1 }; vector<float> P6 = MakeVector(P6arr, 6);
	P[0] = P1; P[1] = P2; P[2] = P3; P[3] = P4; P[4] = P5; P[5] = P6; // Write it all in one 6x6 vector
	return P;
}


vector < vector<float> >tEmatr(float t) // Calculates a 6x6 diagonal matrix with t on the diagonal and -1 on the rest of the matrix
{
	int sizeE = 6;												// Defines the size of the matrix
	vector<vector<float> > E(sizeE, vector<float>(sizeE));		// Iniatilizes the matrix
	for (int m = 0; m < sizeE; ++m)
	{
		for (int n = 0; n < sizeE; ++n)
		{
			if (n == m)
				E[m][n] = t;									// Defines *t* as the element on the diagonal
			else
				E[m][n] = -1;									// Defines -infinity on the rest of the elements (defined as -1 for calculation purposes)
		}
	}
	return E;
}

vector < vector<float> >tEmatrvar(float t, int size) // Calculates a square matrix with t on the diagonal and -1 on the rest of the matrix (with an input for size)
{
	int sizeE = size;										// Uses the size that is supplied by *size*
	vector<vector<float> > E(sizeE, vector<float>(sizeE));	// Initializes the matrix
	for (int m = 0; m < sizeE; ++m)
	{
		for (int n = 0; n < sizeE; ++n)
		{
			if (n == m)
				E[m][n] = t;								// Defines *t* as the element on the diagonal
			else
				E[m][n] = -1;								// Defines -infinity on the rest of the elements (defined as -1 for calculation purposes)
		}
	}
	return E;
}

vector < vector<float> > A0Matr(vector<float> Tau, vector<vector<float> >P) // Calculates the A_0 Matrix using the supplied P-Matrix
{
	vector < vector<float> > Eps = tEmatr(-1);								// Defines the 6x6 -infinity matrix ( Which is defined as -1 for calculation purposes) as Eps (epsilon)
	vector < vector<float> > tfE = tEmatr(Tau[1]);							// Defines the 6x6 -infinity matrix with t_f (ground time) on the diagonal as tfE
	int sizeM = Eps.size();													// Defines sizeM as the one-dimensional size of the epsilon matrix (6)
	vector < vector<float> > A0(2 * sizeM, vector<float>(2 * sizeM));		// Initializes the vector A_0 as a 12x12 Matrix
	for (int m = 0; m < sizeM; ++m)
	{
		for (int n = 0; n < sizeM; ++n)
		{
			A0[m][n] = Eps[m][n];										// Defines the first 6x6 block (B) of the matrix A_0 as Epsilon			[B       C]  == [Epsilon    tf otimes E]									
			A0[m][n + sizeM] = tfE[m][n];								// Defines the second 6x6 block (C) of the matrix A_0 as tfE			|         |  == |					   |
			A0[m + sizeM][n] = P[m][n];									// Defines the third 6x6 block (D) of the matrix A_1 as P				[D		 F]  == [P				Epsilon]
			A0[m + sizeM][n + sizeM] = Eps[m][n];						// Defines the fourth 6x6 block (F) of the matrix A_1 as Epsilon
		}
	}
	return A0;
}

vector < vector<float> > A1Matr(vector<float> Tau, vector<vector<float> >Q) // Calculates the A_1 Matrix using the supplied Q-Matrix
{
	vector < vector<float> > Eps = tEmatr(-1);							// Defines the 6x6 -infinity matrix ( Which is defined as -1 for calculation purposes) as Eps (epsilon)
	vector < vector<float> > tgE = tEmatr(Tau[2]);						// Defines the 6x6 -infinity matrix with t_g (ground time) on the diagonal as tgE
	vector < vector<float> > E = tEmatr(0);							// Defines the 6x6 -infinity matrix with 0 on the diagonal as E
	vector < vector<float> > tgEQ = MPMA(tgE, Q);						// Calculates the Max-Plus matrix addition tgE oplus Q 
	int sizeM = Eps.size();												// Defines sizeM as the one-dimensional size of the epsilon matrix (6)
	vector < vector<float> > A1(2 * sizeM, vector<float>(2 * sizeM));	// Initializes the vector A_1 as a 12x12 Matrix
	for (int m = 0; m < sizeM; ++m)
	{
		for (int n = 0; n < sizeM; ++n)
		{
			A1[m][n] = E[m][n];											// Defines the first 6x6 block (B) of the matrix A_1 as E				[B       C]  == [ E					Epsilon]
			A1[m][n + sizeM] = Eps[m][n];								// Defines the second 6x6 block (C) of the matrix A_1 as Eps			|         |  == |						   |
			A1[m + sizeM][n] = tgEQ[m][n];								// Defines the third 6x6 block (D) of the matrix A_1 as tgEQ			[D		 F]  == [tg otimes E oplus Q	E  ]
			A1[m + sizeM][n + sizeM] = E[m][n];							// Defines the fourth 6x6 block (F) of the matrix A_1 as E
		}
	}
	return A1;
}

vector < vector<float> > KleeneStarOp(vector<vector<float> >A0) // The Kleene Star operation, which calculates: A_0* = sum(0->k) {A_0^k} (for calculation purposes uses k=10)
{
	int k = 10;																					// Defines the k, which defines the amount of iterations used in the Kleene Star algorithm 
	vector<vector< vector<float> > > Ahelp(k + 1, vector<vector<float> >(12, vector<float>(12)));	// Initialize the help-vector which is used to contain A_0^1 -> A_0^k
	Ahelp[0] = A0;																				// Define the first element of the Ahelp vector as A_0^1
	vector<vector<float> > A0star(12, vector<float>(12));											// Initialize A_0*
	A0star = A0;																				// Define A_0* first as the A_0 vector
	for (int n = 0; n < k; ++n)
	{
		Ahelp[n + 1] = MPMM(Ahelp[n], Ahelp[0]);												// Calculates Ahelp[i] as follows: Ahelp[i] = A_0^(i+1)
	}
	for (int m = 0; m < k + 1; ++m)
	{
		A0star = MPMA(Ahelp[m], A0star);														// Sums all Ahelp[i] Matrices to obtain A_0* (without A_0^0)
	}
	vector<vector<float> > E = tEmatrvar(0, 12);													// Calculates the E_(12x12) Matrix (which is A_0^0)
	A0star = MPMA(A0star, E);																	// Sums the A_0* with E to calculate the full A_0*
	return A0star;
}











