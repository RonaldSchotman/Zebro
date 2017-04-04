/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: encoder.h
 *
 * Description:
 * Code to use the rotary absolute encoder
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 */

#ifndef __ENCODER_H_
#define __ENCODER_H_

#define ENCODER_PULSES_PER_ROTATION

#define ENCODER_HALL_PORT PORTB
#define ENCODER_HALL_PIN  PIN2_bm
#define ENCODER_HALL_PINCTRL PIN2CTRL

void encoder_init(void);
//int32_t encoder_get_position(void);
uint8_t encoder_get_hall_state(void);


#endif /* __ENCODER_H_ */