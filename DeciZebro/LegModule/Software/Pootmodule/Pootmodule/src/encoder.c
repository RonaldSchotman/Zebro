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
	/* FIRST initialise the hall-effect sensor */
		/* Set pin as input*/
		ENCODER_HALL_PORT.DIRCLR = ENCODER_HALL_PIN;
		/* turn on pull-up resistor */
		ENCODER_HALL_PORT.ENCODER_HALL_PINCTRL = PORT_OPC_PULLUP_gc;
		
		
	/* SECOND initialise the analog comparator */
	
	///* generate interrupts on both edges of signals */
	//ACA.AC0CTRL |=  AC_INT_MODE_BOTH_EDGES;
	///* set low interrupt level */
	//ACA.AC0CTRL |= AC_INT_LVL_LO;
	///* set high speed mode */
	//ACA.AC0CTRL |= AC_HSMODE_bm;
	///* set large hysteresis */
	//ACA.AC0CTRL |= AC_HYSMODE_LARGE_gc;
	///* Enable Analog Comparator */
	//ACA.AC0CTRL |= AC_ENABLE_bm;
}

/*
 * get state of the hall sensor
 * when magnet present returns 0
 * when magnet absent returns 1
 */	
uint8_t encoder_get_hall_state(void){
	return ((ENCODER_HALL_PORT.IN & ENCODER_HALL_PIN) == ENCODER_HALL_PIN);
	//return 0;
}	
