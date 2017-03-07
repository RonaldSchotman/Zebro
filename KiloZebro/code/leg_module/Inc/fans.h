/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: fans.h
 *
 * Description:
 * Code to drive the cooling fans.
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __FANS_H__
#define __FANS_H__

int32_t fans_set_speed(int32_t speed, int32_t fan);
int32_t fans_calc_speed(int32_t fan);
int32_t fans_calc_and_set_speeds();
void fans_init(void);

#define FANS_PRESCALER 9
#define FANS_ARR 48000

#define FANS_NUM_OF_FANS 2
#define FANS_FAN_1 0
#define FANS_FAN_2 1

#define FANS_MAX_SPEED 100 // percentage
#define FANS_ON_TEMPERATURE  15 // celcius

#define FANS_OUTPUT_1_PIN GPIO_PIN_2
#define FANS_OUTPUT_1_BANK GPIOA
#define FANS_OUTPUT_2_PIN GPIO_PIN_3
#define FANS_OUTPUT_2_BANK GPIOA
#endif /* __FANS_H__ */
