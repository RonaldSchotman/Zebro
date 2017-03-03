/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: main.c
 *
 * Description:
 * Main file for the deci zebro leg module
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 *  
 */
#include <asf.h>
#include "leds.h"

int main (void)
{
	/*some debugging code*/
		/* Initialise system clock */
		sysclk_init();
		/* Initalise delay functions */
		delay_init(sysclk_get_cpu_hz());
	
	/* Initialise board parameters*/
	board_init();
	
	/* Insert application code here, after the board has been initialized. */
		/* Initialise leds */
		leds_init();
		interrupts_enable();
		
		leds_set_LD2();
		leds_blink_LD1_blocking();
	
	
	while (1){
		
	}
}
