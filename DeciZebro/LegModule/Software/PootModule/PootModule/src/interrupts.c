/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: interrupts.c
 *
 * Description:
 * This file helps with enabling and disabling interrupts
 * It keeps a counter of how many times interrupts have been
 * enabled and disabled, so that we do not accidentally enable
 * Interrupts when we should not. For example in nested functions.
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 * 
 */


#include "asf.h"
#include "interrupts.h"

int8_t interrupt_counter = 0;

/**
 * disable interrupts, incrementing counter
 */
int8_t interrupts_disable(void){
	
	Disable_global_interrupt();
	interrupt_counter++;

	return interrupt_counter;
}

/**
 * decrement the interrupt disable counter
 * and enable interrupts when the counter reaches zero
 */
int8_t interrupts_enable(void){
	interrupt_counter--;

	if(interrupt_counter <= 0){
		/* in case strange this have happened, this might fix it */
		interrupt_counter = 0;
		Enable_global_interrupt();
	}

	return interrupt_counter;
}
