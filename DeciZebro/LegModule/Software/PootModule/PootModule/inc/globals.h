/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 
 * Filename: globals.h
 *
 * Description:
 * Defines with global information
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms	-- d.booms@solcon.nl
 */

#ifndef __GLOBALS_H__
#define __GLOBALS_H__


/* every Zebro module has a unique identifier (UID)
 * This UID consists of the following information:
 *
 * Product id:
 * 		8 bit value, identifying the type of module.
 * 		For a leg module, this value is 0
 *
 * Product version:
 * 		The version of this product.
 * 		This is the second leg module, so it is 1
 *
 * Serial id:
 * 		incremenetal serial number. No other module with the same
 * 		product id and version can have the same serial number.
 */

#define GLOBALS_PRODUCT_ID 0
#define GLOBALS_PRODUCT_VERSION 1
#define GLOBALS_SERIAL_ID 1

#define GLOBALS_SOFTWARE_VERSION 0

#define GLOBALS_MOTOR_VOLTAGE 6

/* Define the line bellow to disable the following:
 *  - The watchdog timer
 *  - The emergency break when no clock ticks have been received over
 *    ZebroBus for a while
 * You should only disable this during testing. Seriously.
 */

// #define LIVING_ON_THE_EDGE


#endif /* __GLOBALS_H__ */