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
#include <stdint.h>
#include <asf.h>
#include <avr/io.h>
#include "../inc/clock.h"
#include "../inc/leds.h"
#include "../inc/interrupts.h"
#include "../inc/globals.h"
#include "../inc/vregs.h"
#include "../inc/uart1.h"
#include "../inc/hbridge.h"

int main (void)
{
	/*some debugging code*/
		/* Initialise system clock */
		sysclk_init();
		sysclk_set_source(SYSCLK_SRC_RC32MHZ);
		sysclk_set_prescalers(SYSCLK_PSADIV_1, SYSCLK_PSBCDIV_1_1);
		clock_init();
		/* Initalise delay functions */
		delay_init(sysclk_get_cpu_hz());
	
	/* Initialise board parameters*/
	board_init();
	
	/* Insert application code here, after the board has been initialized. */
		
		leds_init();
		
		vregs_init();
		uart1_init();
		interrupts_enable();
		leds_set_LD1();
		hbridge_init();
		hbridge_sign_magnitude(1, (0xFE));
			
	
	while (1){
		//UART_Transmit(0xAA);
		//UART1_TX_PORT.OUTTGL |= UART1_TX_PIN;
		uart1_send_raw(0xAA);
		delay_ms(1);
		
	}
}
