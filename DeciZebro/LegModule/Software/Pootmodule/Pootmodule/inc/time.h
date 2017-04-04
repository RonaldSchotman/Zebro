/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: time.h
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
 * Daniël Booms -- d.booms@solcon.nl
 */

#ifndef __TIME_H__
#define __TIME_H__

#include "stdint.h"

int32_t time_init(void);
int8_t time_clock_init(void);
//int32_t time_watchdog_init(void);
int8_t time_check_time(void);
int32_t time_get_time_ms(void);
uint8_t time_set_time(uint8_t seconds);
int32_t time_set_clock(void);
int8_t time_counter_reset(void);
//int32_t time_reset_watchdog(void);
int32_t time_dumy_locmotive_controller(void);
int32_t time_calculate_delta(int32_t time_a, int32_t time_b);

#define TIME_ZEBROBUS_TIMEOUT_PERIOD 2048 // /1024 Hz = period in s


#define TIME_ONE_SECOND_COUNTER_VALUE 1024

#define TIME_ROLEOVER_MS 256000
#define TIME_MAX_SECONDS UINT8_MAX

#define TIME_IWDG_REFRESH      (uint32_t)(0x0000AAAA)
#define TIME_IWDG_WRITE_ACCESS (uint32_t)(0x00005555)
#define TIME_IWDG_START        (uint32_t)(0x0000CCCC)
#define TIME_IWDG_RELOAD       2500
#define TIME_MAX_TIME_MS       256000

#endif /* __TIME_H__ */
