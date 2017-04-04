/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: time.c
 *
 * Description:
 * Keeps information about how late it is.
 * Performs emergency stop when we did not receive
 * a command for to long.
 * Also handles the watchdog timer.
 *
 * We use RTC to keep a timebase.
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 * Daniël Booms -- d.booms@solcon.nl
 */

#include <avr/io.h>
#include <asf.h>
#include "../inc/time.h"
#include "../inc/vregs.h"
#include "../inc/leds.h"
#include "../inc/globals.h"
#include "../inc/errors.h"

static uint8_t current_seconds = 0;

/**
 * Initialise the clock timer and the watchdog
 */
int32_t time_init(void){
	time_clock_init();

#ifndef LIVING_ON_THE_EDGE
	//time_watchdog_init();
#endif /* LIVING_ON_THE_EDGE */

	return 0;
}

ISR(RTC_OVF_vect){
	/* Flag is cleared by executing this vector */

#ifndef LIVING_ON_THE_EDGE
	errors_emergency_stop();
	errors_report(ERRORS_ZEBROBUS_NO_TIMING_INFO);
#endif /* LIVING_ON_THE_EDGE */

}

int8_t time_clock_init(void){

	/* enable the 1.024 kHz clock to RTC32 */
	sysclk_rtcsrc_enable(SYSCLK_RTCSRC_RCOSC);
	/* UEV events generated only by overflows */
	RTC.INTCTRL |= RTC_OVFINTLVL_HI_gc;
	/* set the period*/
	RTC.PER = TIME_ZEBROBUS_TIMEOUT_PERIOD;
	/* start counting at 0 */
	RTC.CNT = 0;
	/* enable the counter */
	RTC.CTRL |= RTC_PRESCALER_DIV1_gc;


	return 0;
}

/**
 * Reset the counter of the clock to zero
 */
int8_t time_counter_reset(void){
	RTC.CNT = 0;

	return 0;
}


/**
 * Write the value of the counter to the vregs
 */
int8_t time_check_time(void){
	uint16_t counter_value;

	counter_value = RTC.CNT;
	vregs_write(VREGS_CLOCK_A, (uint8_t) (counter_value >> 8));
	vregs_write(VREGS_CLOCK_B, (uint8_t) counter_value);
	vregs_write(VREGS_SYNC_COUNTER, (uint8_t) current_seconds);

	return 0;
}

/**
 * Get the current time in ms
 */
int32_t time_get_time_ms(void){
	int32_t time;

	time = current_seconds * 1000;
	time = time + ((RTC.CNT * 1000) / TIME_ONE_SECOND_COUNTER_VALUE);

	return time;
}

/**
 * Set the current time, to a certain amount of seconds.
 * Fractional seconds are set to 0.
 */
uint8_t time_set_time(uint8_t seconds){
	current_seconds = seconds;
	RTC.CNT = 0;

	return seconds;
}

/**
 * Demo thingy to make the clock count up, when no locomotive controller is
 * present.
 */
int32_t time_dumy_locmotive_controller(void){
	if (RTC.CNT >= TIME_ONE_SECOND_COUNTER_VALUE){
		time_counter_reset();
		current_seconds = (current_seconds + 1) % TIME_MAX_SECONDS;
	}

	return 0;
}

/**
 * Get the time time_a - time_b
 * When this difference is larger than TIME_ROLEOVER_MS / 2,
 * we assume that a rollover has occurred.
 */
int32_t time_calculate_delta(int32_t time_a, int32_t time_b){
	int32_t delta;

	delta = time_a - time_b;

	if (delta < - TIME_ROLEOVER_MS / 2) delta = delta + TIME_ROLEOVER_MS;
	if (delta > TIME_ROLEOVER_MS / 2) delta = delta - TIME_ROLEOVER_MS;

	return delta;

}

/**
 * Initialise the watchdog timer
 */
//int32_t time_watchdog_init(void){
	  ///* (1) Activate IWDG (not needed if done in option bytes) */
	  ///* (2) Enable write access to IWDG registers */
	  ///* (3) Set prescaler by 8 */
	  ///* (4) Set reload value to have a rollover each 100ms */
	  ///* (5) Check if flags are reset */
	  ///* (6) Refresh counter */
	  //IWDG->KR = TIME_IWDG_START; /* (1) */
	  //IWDG->KR = TIME_IWDG_WRITE_ACCESS; /* (2) */
	  //IWDG->PR = IWDG_PR_PR_1; /* (3) */
	  //IWDG->RLR = TIME_IWDG_RELOAD; /* (4) */
	  //while(IWDG->SR); /* (5) */
	//return 0;
//}

/**
 * Let the watchdog know that we are still alive and kicking
 */
//int32_t time_reset_watchdog(void){
	//IWDG->KR = TIME_IWDG_REFRESH;
	//return 0;
//}

