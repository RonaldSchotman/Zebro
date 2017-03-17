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
#include <avr/io.h>
#include "../inc/leds.h"
#include "../inc/interrupts.h"
#include "../inc/globals.h"
#include "../inc/vregs.h"
#include "../inc/uart1.h"
#include "UART_portD.h"
#include "LightweightRingBuff.h"

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
		vregs_init();
		uart_init();
		//UART1_TX_PORT.DIR |= UART1_TX_PIN;
		leds_set_LD1();
			
	
	while (1){
		UART_Transmit(0xAA);
		//UART1_TX_PORT.OUTTGL |= UART1_TX_PIN;
		delay_ms(1);
		
	}
}
