/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 
 * Filename: clock.c
 *
 * Description:
 * Configures global clock settings
 *
 * Authors:
 * Martijn de Rooij -- 
 * Daniel Booms	-- d.booms@solcon.nl
 */

#include <stdint.h>
#include <avr/io.h>
#include "../inc/clock.h"

void clock_init(void)
{
	CCP = CCP_IOREG_gc;
	OSC.CTRL |= OSC_RC32MEN_bm;
	while(!(OSC.STATUS & OSC_RC32MRDY_bm));
	CCP = CCP_IOREG_gc;
	CLK.CTRL = CLK_SCLKSEL_RC32M_gc;
}
