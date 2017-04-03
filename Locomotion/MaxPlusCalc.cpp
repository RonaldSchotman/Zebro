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
// In this file, all necessary functions for max-plus operations are determined
//-------------------------------------------------------------------------------------------------------------------------------------------------
// MAX and MIN vector calculations (yeah, I needed three functions to achieve the result of 1 function, and no, I'm not proud of myself)
float maxvecfloat(vector<float> v)
{
float z=0;
for (unsigned int m=0;m<v.size();++m)
{
if (z<v[m])
z = v[m];
}
return z;
}

double maxvec(vector<double> v) //This function calculates the maximum value of a vector, further used in the max-plus calculations for matrices and vectors
{
double z = 0;
for (unsigned int m = 0; m < v.size(); ++m)
{
if (z < v[m])
z = v[m];
}
return z;
}

float MaxVec(vector<float>A) // Calculates the maximum value of a vector
{
	float C = -1;					// Initializes C as -1 (or minus infinity for our purpose)
	int SizeV = A.size();			// Initializes SizeV as the size of the vector A
	for (int m = 0; m < SizeV; ++m)
	{
		if (C < A[m])
			C = A[m];				// Uses iteration to find the highest value of C
	}
	return C;						// Outputs C
}

float MinVec(vector<float>A) // Calculates the maximum value of a vector
{
	float C = A[0];					// Initializes C as -1 (or minus infinity for our purpose)
	int SizeV = A.size();			// Initializes SizeV as the size of the vector A
	for (int m = 0; m < SizeV; ++m)
	{
		if (C > A[m])
			C = A[m];				// Uses iteration to find the highest value of C
	}
	return C;						// Outputs C
}

//-------------------------------------------------------------------------------------------------------------------------------------------------
// Max-Plus Matrix times Vector (A x v1 = v2) calculation (again two functions for the same idea. Cant be bothered to find out which one is irrelevant
vector<double> mpmatrixvecmult(double matr[][12], vector<double> vect) // This function multiplies a matrix and a vector with Max-Plus algebra ( in the following order: Matrix (OTIMES) Vector = Vector ) using the maxvec function
{
vector <double> vecout(12, 0);
for (int i = 0; i < 12; ++i)
{
vector <double> helpvec(12, -1);
for (int j = 0; j < 12; ++j)
{
if (matr[i][j] > -1)
{
helpvec[j] = matr[i][j] + vect[j];
}
else
{
helpvec[j] = -1;
}
}
vecout[i] = maxvec(helpvec);
}
return vecout;
}

vector<float> MPMVM(vector<vector<float> > A, vector<float> B) // Calculates the Max-Plus matrix vector multiplication
{
	int SizeM = A.size();				// Defines SizeM as the one-dimensional size of matrix A
	vector<float> C(SizeM);				// Initializes output vector C
	for (int m = 0; m < SizeM; ++m)
	{
		C[m] = MPVM(A[m], B);			// Uses the MPVM function to calculate the seperate elements of C
	}
	return C;							// Outputs C
}

//-------------------------------------------------------------------------------------------------------------------------------------------------
// Max-Plus Vector multiplication (Max-Plus dot-product in a way) (V1' times V2 = [v11,v12] * [v21;v22] = max(v11,v21)+max(v12,v22))  
float MPVM(vector<float> A, vector<float> B)	// Calculates the Max-Plus vector multiplication of vertical vector A and horizontal vector B as -> A \otimes B = C
{
	int SizeV = A.size();			// Define SizeV as the size of the vector A
	vector<float> help(SizeV);		// Initializes the help vector
	for (int m = 0; m < SizeV; ++m)
	{
		if (A[m] < 0 || B[m] < 0)
			help[m] = -1;			// Instead of using the minus infinity for calculating with the Max-Plus element epsilon, the -1 is used to reduce the calculational load. t \otimes -1 = -1 as t \otimes -infinity = -infinity
		else
			help[m] = A[m] + B[m];  // Calculates the element A[m] \otimes B[m] = help[m] as A[m]+B[m]=help[m]
	}
	float C = MaxVec(help);			// Calculates the maximum value of the help vector to define C
	return C;						// Outputs C
}

//-------------------------------------------------------------------------------------------------------------------------------------------------
// Max-Plus Matrix Addition function
vector<vector<float> > MPMA(vector<vector<float> >A, vector<vector<float> >B) // Calculates the Max-Plus matrix addition as -> A oplus B = C
{
	int SizeM = A.size();									// Defines SizeM as the one-dimensional size of the matrix A
	vector<vector<float> > C(SizeM, vector<float>(SizeM));	// Initializes output C
	for (int m = 0; m < SizeM; ++m)
	{
		for (int n = 0; n < SizeM; ++n)
		{
			if (A[m][n] > B[m][n])
				C[m][n] = A[m][n];							// If the element A[m][n] is bigger than the element B[m][n], the element C[m][n] becomes A[m][n]
			else
				C[m][n] = B[m][n];							// Else, if the element A[m][n] is smaller of equal to the element B[m][n], C[m][n] becomes B[m][n]
		}
	}
	return C;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------
// Max-Plus Matrix Multiplication function
vector<vector<float> > MPMM(vector<vector<float> >A, vector<vector<float> >B) // Calculates the Max-Plus matrix multiplication as -> A otimes B=C
{
	int SizeM = A.size();										// Defines SizeM as the one-dimensional size of the Matrix
	vector<vector<float> > C(SizeM, vector<float>(SizeM));		// Initializes output C
	vector<vector<float> > D(SizeM, vector<float>(SizeM));		// Initializes help-matrix D
	for (int m = 0; m < SizeM; ++m)
	{
		for (int n = 0; n < SizeM; ++n)
		{
			D[n][m] = B[m][n];									// Calculates D as the transpose of B to make the ith elements of the vectors of B into i vectors
		}
	}
	for (int m = 0; m < SizeM; ++m)
	{
		for (int n = 0; n < SizeM; ++n)
		{
			C[m][n] = MPVM(A[m], D[n]);							// Uses the MPVM function to calculate the seperate elements of matrix C
		}
	}
	return C;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------
// Max-Plus vector multiplication elementwise (or the standard vector addition)
vector<float> VAdd(vector<float> A, vector<float> B) // Adds the elements of vector a and b to make vector c
{
	int SizeV = A.size();
	vector <float> C(SizeV);
	for (int i = 0; i < SizeV; ++i)
	{
		C[i] = A[i] + B[i];
	}
	return C;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------------------------------------------------------------
