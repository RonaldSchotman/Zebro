/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: interupts.c
 *
 * Description:
 * This file helps with enabling and disabling interrupts
 * It keeps a counter of how many times interrupts have been
 * enabled and disables, so that we do not accidently enable
 * Interrupts when we should not. For example in nested functions.
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#include "stm32f0xx_hal.h"
#include "stdint.h"

int32_t interupt_counter = 0;

/**
 * disable interrupts, incrementing counter
 */
int32_t interrupts_disable(){
	__disable_irq();
	interupt_counter++;

	return interupt_counter;
}

/**
 * decrement the interrupt disable counter
 * and enable interrupts when the counter reaches zero
 */
int32_t interrupts_enable(){
	interupt_counter--;

	if(interupt_counter <= 0){
		/* in case strange this have happened, this might fix it */
		interupt_counter = 0;
		__enable_irq();
	}

	return interupt_counter;
}
