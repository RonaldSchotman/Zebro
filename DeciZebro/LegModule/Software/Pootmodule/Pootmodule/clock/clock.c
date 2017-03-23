/*
 * clock.c
 *
 * Created: 19-2-2014 11:44:20
 *  Author: Martijn
 */ 

#include <avr/io.h>


void Config32MHzClock(void)
{
	CCP = CCP_IOREG_gc;
	OSC.CTRL |= OSC_RC32MEN_bm;
	while(!(OSC.STATUS & OSC_RC32MRDY_bm));
	CCP = CCP_IOREG_gc;
	CLK.CTRL = CLK_SCLKSEL_RC32M_gc;
}

int main(void)
{
	while(1)
	{
		asm volatile ("nop");
	}
}