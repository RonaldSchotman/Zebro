/**
 * POOT / DECI ZEBRO LEG MODULE
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: errors.c
 *
 * Description:
 * Code to handle error reporting
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#include <stdint.h>

#include "../inc/errors.h"
#include "../inc/interrupts.h"
#include "../inc/vregs.h"
#include "../inc/hbridge.h"


static uint8_t error_counter = 0;
static uint8_t last_error = 0;
static int32_t errors_array[ERRORS_NUM_OF_ERRORS];
static int32_t emergency_stop = 0;

// TODO, enable resetting of errors via ZebroBus

/**
 * Initialise the array that stores what errors were reported
 */
void errors_init(void){
	int32_t cursor;

	for(cursor = 0; cursor < ERRORS_NUM_OF_ERRORS; cursor ++){
		errors_array[cursor] = 0;
	}
}

int32_t errors_reset_errors(int32_t safety){
	int32_t cursor;

	if (safety != ERRORS_ERRORS_RESET_SAFETY)
		return 1;

	/**
	 * BEGIN critical section
	 */
	interrupts_disable();

	error_counter = 0;
	last_error = 0;

	for(cursor = 0; cursor < ERRORS_NUM_OF_ERRORS; cursor ++){
		errors_array[cursor] = 0;
	}

	vregs_write(VREGS_ERROR_COUNTER, error_counter);
	vregs_write(VREGS_LAST_ERROR, last_error);
	vregs_write(VREGS_EMERGENCY_STOP, emergency_stop);

	interrupts_enable();
	/**
	 * END critical section
	 */

	return 0;

}
/**
 * Perform an emergency stop
 */
int32_t errors_emergency_stop(void){
	hbridge_disable();
	emergency_stop = 1;
	//motion_stop();
	vregs_write(VREGS_EMERGENCY_STOP, 1);
	return 0;
}

/**
 * Returns true when the system is an emergency stop state
 */
int32_t errors_check_for_emergency_stop(void){
	return emergency_stop;
}

/**
 * Clear an emergency stop.
 * Only call this function if you are _certain_ about what
 * you are doing!
 */
int32_t errors_reset_emergency_stop(int32_t safety){
	if (safety != ERRORS_EMERGENCY_STOP_SAFETY){
		errors_emergency_stop();
		errors_report(ERRORS_EMERGENCY_STOP_RESET_ERROR);
		return 1;
	}
	emergency_stop = 0;
	vregs_write(VREGS_EMERGENCY_STOP, 0);

	return 0;
}


/**
 * Used by various functions / tasks to report errors.
 * We disable interrupts, so the function can also be called from
 * interrupt routines.
 */
void errors_report(uint8_t error_number){

	/**
	 * BEGIN critical section
	 */
	interrupts_disable();

	/* check what errors where already reported */
	if(errors_array[error_number - 1] == 0){
		error_counter++;

	}
	errors_array[error_number - 1] = 1;

	last_error = error_number;

	vregs_write(VREGS_ERROR_COUNTER, error_counter);
	vregs_write(VREGS_LAST_ERROR, error_number);

	interrupts_enable();
	/**
	 * END critical section
	 */
}
