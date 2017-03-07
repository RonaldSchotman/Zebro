/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: leds.h
 *
 * Description:
 * Code to drive the LEDs
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __LEDS_H__
#define __LEDS_H__

#define LD3_PIN GPIO_PIN_9
#define LD4_PIN GPIO_PIN_8
#define LD3_BANK GPIOC
#define LD4_BANK GPIOC

#define LEDS_H_BLINK_SPEED 500

void leds_init();
void leds_set_LD3();
void leds_clear_LD3();
void leds_toggle_LD3();
void leds_blink_LD3_blocking();
void leds_set_LD4();
void leds_clear_LD4();
void leds_toggle_LD4();
void leds_blink_LD4_blocking();

#endif /* __LEDS_H_ */
