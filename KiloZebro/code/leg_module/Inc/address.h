/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: address.h
 *
 * Description:
 * Finds out where on the Zebro chassis the module was connected
 * and determines what the correct ZebroBus address is.
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __ADDRESS_H__
#define __ADDRESS_H__

#include "zebrobus.h"

int32_t address_init(void);
int32_t address_measure_position(void);
int32_t address_get_position(void);
int32_t address_get_side(void);
int32_t address_get_zebrobus_address(void);
void address_write_to_vregs(void);

#define ADDRESS_LEFT_0 0
#define ADDRESS_LEFT_1 1
#define ADDRESS_LEFT_2 2
#define ADDRESS_LEFT_3 3
#define ADDRESS_LEFT_4 4
#define ADDRESS_LEFT_5 5
#define ADDRESS_RIGHT_0 6
#define ADDRESS_RIGHT_1 7
#define ADDRESS_RIGHT_2 8
#define ADDRESS_RIGHT_3 9
#define ADDRESS_RIGHT_4 10
#define ADDRESS_RIGHT_5 11

#define ADDRESS_NUMBER_OF_POSITIONS 12

#define ADDRESS_LEFT 0
#define ADDRESS_RIGHT 1

#define ADDRESS_ZEBROBUS_OFFSET 0x10
#define ADDRESS_BROADCAST_ADDRESS 0x0


#endif  /* __ADDRESS_H__ */
