/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: hbridge.h
 *
 * Description:
 * Code to drive the h-bridge
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 */

#ifndef __HBRIDGE_H__
#define __HBRIDGE_H__


#define HBRIDGE_PERIOD		8192		  //32MHz/8192/2*8(for the HRES extension) = 15.6kHz 
#define HBRIDGE_PORT		PORTC
#define HBRIDGE_PIN_1		PIN3_bm
#define HBRIDGE_PIN_2		PIN5_bm
#define HBRIDGE_PIN_2_CTRL	PIN5CTRL

void hbridge_init(void);
void hbridge_disable(void);
void hbridge_lock_anti_phase(uint16_t dutycycle);
void hbridge_sign_magnitude(uint8_t direction, uint16_t dutycycle);



#endif /* __HBRIDGE_H__ */