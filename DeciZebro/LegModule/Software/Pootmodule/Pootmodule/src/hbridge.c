/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: hbridge.c
 *
 * Description:
 * Code to drive the h-bridge
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 */

#include <stdint.h>
#include <asf.h>
#include "../inc/hbridge.h"



/**
 * Initialses the h-bridge timers and GPIO
 */
void hbridge_init(void){
	/* For the driving the H bridge, the the CHB and CHC output compare
	 * channels of TIM0 are used.
	 * They are connected to the H bridge as follows:
	 *                            ^ + VBAT
     *                     	   	  |
     *              |-----------------------------|
     *              |                             |
     *              |                             |
     *              |                             |
     *        Q1 ||--                             --|| Q3
     *   CHA ----||                                 ||---- ~CHA/PIN5
     *   /PIN3   ||--                             --|| 
     *              |               --------      |
     *              |        /-\   |        |     |
     *              |-------| M |--| ACS711 |-----|
     *              |        \-/   |        |     |
     *              |               --------      |
     *        Q2 ||--                             --|| Q4
     *  ~CHA ----||                                 ||---- CHA/PIN5
     *   /PIN3   ||--                             --|| 
     *              |                             |
     *              |                             |
     *              |                             |
     *              |-----------------------------|
     *                             |
     *                            --- GND
     *
     * After initialisation,  Q2 and Q4 are turned on,
     * so the motor is short circuited.
     *  
	 */
	
	/* Configure the timer */
		/* Enable the clock */
		sysclk_enable_module(SYSCLK_PORT_C, SYSCLK_TC0);
		sysclk_enable_module(SYSCLK_PORT_C, SYSCLK_HIRES);
		
		/* Set waveform generator mode to dual slope PWM
		 * that is: center aligned PWM, with events during the dead time */
		TCC0.CTRLB |= TC0_WGMODE2_bm | TC0_WGMODE0_bm;
		
		/* Set timer period */
		TCC0.PER = HBRIDGE_PERIOD;
		
		/* Enable Compare mode on channel A */
		TCC0.CTRLB |= TC0_CCAEN_bm;
		
		/* Configure advanced waveform extension mode */
			/* Set pattern generation mode and Common Waveform Channel Mode*/
			AWEXC.CTRL = AWEX_PGM_bm |  AWEX_DTICCAEN_bm | AWEX_DTICCBEN_bm | AWEX_DTICCCEN_bm | AWEX_DTICCDEN_bm;//AWEX_CWCM_bm |
			/* Set out bit of the uninverted pin to short the motor */
			HBRIDGE_PORT.OUTSET = HBRIDGE_PIN_1;
			HBRIDGE_PORT.OUTCLR = HBRIDGE_PIN_2;
					
		/* Set high resolution plus mode on timer 0 */
		HIRESC.CTRLA |= HIRES_HREN0_bm | HIRES_HRPLUS_bm;
		
		/* Set interrupts */
		//TODO: Write ADC trigger on timer interrupt
		
		/* Set clock to unprescaled clock, enabling the timer */
		TCC0.CTRLA |= TC0_CLKSEL0_bm;
	
		
	/* Configure the GPIO pins */
		/* Set pins to output */
		HBRIDGE_PORT.DIRSET = HBRIDGE_PIN_1 | HBRIDGE_PIN_2;
		/* Set one of the pins to inverted polarity */
		HBRIDGE_PORT.HBRIDGE_PIN_2_CTRL |= PORT_INVEN_bm;
}

/** 
 * Short the motor to the ground rail
 */
void hbridge_disable(void){
	/* Disable the timer outputs */
	AWEXC.OUTOVEN &= ~(HBRIDGE_PIN_1 | HBRIDGE_PIN_2);
	/* Set the outputs to 0 and 1  
	 * shorting the motor to the ground rail */
	HBRIDGE_PORT.OUTSET = HBRIDGE_PIN_1;
	HBRIDGE_PORT.OUTCLR = HBRIDGE_PIN_2;
}

/** 
 * Drive the motor in lock anti phase mode
 * the outputs on both channels are the same but channel C is inverted in the GPIO unit
 * the dutycycle should be a 13 bit left-aligned value
 * 
 */
void hbridge_lock_anti_phase(uint16_t dutycycle){
	/* Set the output compare value to the dutycycle */
	TCC0.CCA = (dutycycle>>3);
	/* Enable timer outputs */
	AWEXC.OUTOVEN |= (HBRIDGE_PIN_1 | HBRIDGE_PIN_2);
}

void hbridge_sign_magnitude(uint8_t direction, uint16_t dutycycle){
	/* Set the output compare value to the dutycycle */
	TCC0.CCA = (dutycycle>>3);
	/* Enable timer output on pin 2, disable on pin 1 */
	AWEXC.OUTOVEN |= HBRIDGE_PIN_2;
	AWEXC.OUTOVEN &= ~HBRIDGE_PIN_1;
	/* Set out bit of the uninverted pin to set direction*/
	if (direction) {
		HBRIDGE_PORT.OUTSET = HBRIDGE_PIN_1;
	}
	else {
		HBRIDGE_PORT.OUTCLR = HBRIDGE_PIN_1;
	}
}

