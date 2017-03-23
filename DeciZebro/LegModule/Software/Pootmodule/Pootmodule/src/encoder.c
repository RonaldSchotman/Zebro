/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: encoder.c
 *
 * Description:
 * Code to use the rotary absolute encoder
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 */

#include "avr/io.h"
#include "asf.h"
#include "../inc/encoder.h"

/* this function initialises the Analog Compare Unit 0 at port A */
void encoder_init(void){
	/* generate interrupts on both edges of signals */
	ACA.AC0CTRL |=  AC_INT_MODE_BOTH_EDGES;
	/* set low interrupt level */
	ACA.AC0CTRL |= AC_INT_LVL_LO;
	/* set high speed mode */
	ACA.AC0CTRL |= AC_HSMODE_bm;
	/* set large hysteresis */
	ACA.AC0CTRL |= AC_HYSMODE_LARGE_gc;
	/* Enable Analog Comparator */
	ACA.AC0CTRL |= AC_ENABLE_bm;
	
	
}