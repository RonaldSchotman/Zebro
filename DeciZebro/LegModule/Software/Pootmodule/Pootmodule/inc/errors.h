/**
 * POOT / DECI ZEBRO LEG MODULE
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: errors.h
 *
 * Description:
 * Header to handle error reporting
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __ERRORS_H__
#define __ERRORS_H__

void errors_init(void);
void errors_report(uint8_t error_number);
int32_t errors_emergency_stop(void);
int32_t errors_check_for_emergency_stop(void);
int32_t errors_reset_emergency_stop(int32_t safety);
int32_t errors_reset_errors(int32_t safety);

#define ERRORS_NUM_OF_ERRORS 9
#define ERRORS_POOTBUS_ERROR 1
#define ERRORS_POOTBUS_NACK 2
#define ERRORS_POOTBUS_UNEXPECTED 3
#define ERRORS_POOTBUS_TIMOUT 4
#define ERRORS_MOTOR_OVERTEMPERATURE 5
#define ERRORS_MOTOR_OVERCURRENT 6
#define ERRORS_ZEBROBUS_NO_TIMING_INFO 7
#define ERRORS_EMERGENCY_STOP_RESET_ERROR 8
#define ERRORS_WALK_TIMOUT_ERROR 9

#define ERRORS_EMERGENCY_STOP_SAFETY 0x12

#define ERRORS_ERRORS_RESET_SAFETY 0x56

#endif /* __ERRORS_H__ */
