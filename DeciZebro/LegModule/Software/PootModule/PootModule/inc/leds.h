/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: leds.h
 *
 * Description:
 * Code to drive the LEDs
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 * 
 */

#ifndef __LEDS_H__
#define __LEDS_H__

/**
 * Location of Led 1 is Port E Pin 3
 * Location of Led 2 is Port D Pin 0 
 */
#define LEDS_LD1_PIN			PIN3_bm
#define LEDS_LD2_PIN			PIN0_bm
#define LEDS_LD1_PORT			PORTE
#define LEDS_LD2_PORT			PORTD

#define LEDS_H_BLINK_SPEED		500 // milliseconds


void leds_init();
void leds_set_LD1();
void leds_clear_LD1();
void leds_toggle_LD1();
void leds_blink_LD1_blocking();
void leds_set_LD2();
void leds_clear_LD2();
void leds_toggle_LD2();
void leds_blink_LD2_blocking();

#endif /* __LEDS_H_ */
