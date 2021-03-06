/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: adc.c
 *
 * Description:
 * Keeps information about how late it is.
 * Performs emergency stop when we did not receive
 * a command for to long
 * Also handles the watchdog timer
 *
 * We use timer 16 to keep a timebase.
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __TIME_H__
#define __TIME_H__

#include "stdint.h"

int32_t time_init(void);
int32_t time_clock_init(void);
uint8_t time_clock_17_init(void);
uint8_t time_clock_6_init(void);
int32_t time_watchdog_init(void);
uint16_t time_check_time(void);
uint32_t time_get_time_ms(void);
uint16_t time17_get_time(void);
uint8_t get_current_seconds(void);
uint8_t time_set_time(uint8_t seconds);
int32_t time_set_clock(void);
int32_t time_counter_reset(void);
int32_t time_reset_watchdog(void);
uint8_t time_dumy_locmotive_controller(void);
int32_t time_calculate_delta(int32_t time_a, int32_t time_b);
void start_timing_measurement(void);
int8_t stop_and_return_timing_measurement(int32_t delta);
void reset_timing_measurement(void);

//#define TIME_CLOCK_PRESCALER 3661
#define TIME_CLOCK_PRESCALER 749
//#define TIME_ONE_SECOND_COUNTER_VALUE 13108
#define TIME_ONE_SECOND_COUNTER_VALUE 64000
#define TIME_EMERGENCY_STOP_PRIORITY 0
#define TIME_ROLEOVER_MS 256000 // 256 * 1000
#define TIME_MAX_SECONDS UINT8_MAX

#define TIME_IWDG_REFRESH      (uint32_t)(0x0000AAAA)
#define TIME_IWDG_WRITE_ACCESS (uint32_t)(0x00005555)
#define TIME_IWDG_START        (uint32_t)(0x0000CCCC)
#define TIME_IWDG_RELOAD       2500
#define TIME_MAX_TIME_MS       256000

#endif /* __TIME_H__ */
