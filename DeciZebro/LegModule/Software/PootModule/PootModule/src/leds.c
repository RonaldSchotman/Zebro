/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: leds.c
 *
 * Description:
 * Code to drive the LEDs
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 * 
 */

#include "asf.h"
#include "leds.h"

/** 
 * Initialise the leds
 * configure output pins
 */
void leds_init(void){
	/* Configure pins as output, write '1' to direction register */
	LEDS_LD1_PORT.DIR |= LEDS_LD1_PIN;
	LEDS_LD2_PORT.DIR |= LEDS_LD2_PIN;
	/* Turn leds off, write '1' to output clear register*/
	LEDS_LD1_PORT.OUTCLR |= LEDS_LD1_PIN;
	LEDS_LD2_PORT.OUTCLR |= LEDS_LD2_PIN;
	
	//PORTD_PIN0CTRL |= PORT_OPC_WIREDORPULL_gc;
	//PORTE_PIN3CTRL |= PORT_OPC_WIREDORPULL_gc;
}

/** 
 * Turn LED 1 on
 */
void leds_set_LD1(void){
	LEDS_LD1_PORT.OUTSET |= LEDS_LD1_PIN;
}

/** 
 * Turn LED 1 off
 */
void leds_clear_LD1(void){
	LEDS_LD1_PORT.OUTCLR |= LEDS_LD1_PIN;
}

/** 
 * Toggle LED 1
 */
void leds_toggle_LD1(void){
	LEDS_LD1_PORT.OUTTGL |= LEDS_LD1_PIN;
}

/** 
 * Blink LED 1 indefinitely while blocking all other MCU activity
 * Use only during debugging
 */
void leds_blink_LD1_blocking(void){
	while (1)
	{
		LEDS_LD1_PORT.OUTTGL |= LEDS_LD1_PIN;
		delay_ms(LEDS_H_BLINK_SPEED);
	}
}

/** 
 * Turn LED 2 on
 */
void leds_set_LD2(void){
	LEDS_LD2_PORT.OUTSET |= LEDS_LD2_PIN;
}

/** 
 * Turn LED 2 off
 */
void leds_clear_LD2(void){
	LEDS_LD2_PORT.OUTCLR |= LEDS_LD2_PIN;
}

/** 
 * Toggle LED 2
 */
void leds_toggle_LD2(void){
	LEDS_LD2_PORT.OUTTGL |= LEDS_LD2_PIN;
}

/** 
 * Blink LED 2 indefinitely while blocking all other MCU activity
 * Use only during debugging
 */
void leds_blink_LD2_blocking(void){
	while (2)
	{
		LEDS_LD2_PORT.OUTTGL |= LEDS_LD2_PIN;
		delay_ms(LEDS_H_BLINK_SPEED);
	}
}