/**
 * \file
 *
 * \brief Empty user application template
 *
 */

/**
 * \mainpage User Application template doxygen documentation
 *
 * \par Empty user application template
 *
 * Bare minimum empty user application template
 *
 * \par Content
 *
 * -# Include the ASF header files (through asf.h)
 * -# "Insert system clock initialization code here" comment
 * -# Minimal main function that starts with a call to board_init()
 * -# "Insert application code here" comment
 *
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */
/*
 * Support and FAQ: visit <a href="http://www.atmel.com/design-support/">Atmel Support</a>
 */
#include <asf.h>

int main (void)
{
	/* Insert system clock initialization code here (sysclk_init()). */
	//sysclk_init();

	board_init();


	PORTD_DIR |= PIN0_bm;
	PORTD_OUT |= PIN0_bm;
	PORTD_PIN0CTRL |= PORT_OPC_WIREDORPULL_gc;
	PORTE_DIR |= PIN3_bm;
	PORTE_OUT |= PIN3_bm;
	PORTE_PIN3CTRL |= PORT_OPC_WIREDORPULL_gc;	
	/* Insert application code here, after the board has been initialized. */
	
	while (1){
		
	}
}
