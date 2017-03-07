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
 * The ZebroBus uses the I2C1 bus
 *
 * @author Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __ZEBROBUS_H__
#define __ZEBROBUS_H__

#include "stdint.h"

#define ZEBROBUS_SDA_PIN GPIO_PIN_7
#define ZEBROBUS_SDA_BANK GPIOB
#define ZEBROBUS_SCL_PIN GPIO_PIN_8
#define ZEBROBUS_SCL_BANK GPIOB

#define ZEBROBUS_OWN_ADDRESS 0b10011110

#define ZEBROBUS_STATE_IDLE 0
#define ZEBROBUS_STATE_RECEIVED_ADDR 1

#define ZEBROBUS_SIZE_OF_QUEUE 50
#define ZEBROBUS_QUEUE_FULL 1

struct zebrobus_write_request{
     uint32_t address;
	 uint8_t data;
};

int32_t zebrobus_slave_init();
int32_t zebrobus_put_write_request(uint32_t address, uint8_t data);
struct zebrobus_write_request zebrobus_get_write_request();
int32_t zebrobus_process_write_requests();

#endif /* __ZEBROBUS_H__ */
