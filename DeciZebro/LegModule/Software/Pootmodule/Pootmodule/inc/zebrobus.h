/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: zebrobus.h
 *
 * Description:
 * Header for the interface with the ZebroBus
 * The ZebroBus uses the TWIE bus
 *
 * author
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms -- d.booms@solcon.nl
 */

#ifndef __ZEBROBUS_H__
#define __ZEBROBUS_H__

#include "stdint.h"

#define ZEBROBUS_SDA_PIN		PIN0_bm
#define ZEBROBUS_SDA_PINCTRL	PIN0CTRL
#define ZEBROBUS_PORT			PORTE
#define ZEBROBUS_SCL_PIN		PIN1_bm
#define ZEBROBUS_SCL_PINCTRL	PIN1CTRL
#define ZEBROBUS_ENABLE_PIN		PIN2_bm

#define ZEBROBUS_OWN_ADDRESS 0b10011110

#define ZEBROBUS_STATE_IDLE 0
#define ZEBROBUS_STATE_RECEIVED_ADDR 1

#define ZEBROBUS_SIZE_OF_QUEUE 50
#define ZEBROBUS_QUEUE_FULL 1

#define ZEBROBUS_GENERAL_CALL_ENABLE 0x01

struct zebrobus_write_request{
     uint32_t address;
	 uint8_t data;
};

int8_t zebrobus_slave_init(void);
int8_t zebrobus_put_write_request(uint32_t address, uint8_t data);
struct zebrobus_write_request zebrobus_get_write_request(void);
int32_t zebrobus_process_write_requests(void);

#endif /* __ZEBROBUS_H__ */
