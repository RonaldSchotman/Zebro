/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: pootbus.h
 *
 * Description:
 * Header for the interface with the PootBus
 * The PootBus uses the I2C2 bus
 *
 * @author Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __POOTBUS_H__
#define __POOTBUS_H__

#define POOTBUS_SDA_PIN GPIO_PIN_11
#define POOTBUS_SDA_BANK GPIOB
#define POOTBUS_SCL_PIN GPIO_PIN_10
#define POOTBUS_SCL_BANK GPIOB

#define POOTBUS_BUS_BUSY 1
#define POOTBUS_BAD_ADDRESS 2
#define POOTBUS_TIMEOUT 3

#define POOTBUS_MAX_TRANSACTION_TIME 1000

#define POOTBUS_IRQ_PRIORITY 4

#define POOTBUS_STATE_IDLE 0
#define POOTBUS_TEMP_SEND_ADDRESS 1
#define POOTBUS_TEMP_RECEIVE_BYTE_1 2
#define POOTBUS_TEMP_RECEIVE_BYTE_2 3

#define POOTBUS_TEMP_DATA_ADDRESS 0x00

#define POOTBUS_TEMPSENSOR_111_ADR 0b10011110
#define POOTBUS_TEMPSENSOR_111_DEST 0
#define POOTBUS_TEMPSENSOR_100_ADR 0b10011000
#define POOTBUS_TEMPSENSOR_100_DEST 1

#define POOTBUS_NUM_OF_SENSORS 2
#define POOTBUS_NUM_OF_BYTES 2

#define POOTBUS_NUM_OF_TEMP_SENSORS POOTBUS_NUM_OF_SENSORS
#define POOTBUS_EMERGENCY_MOTOR_TEMPERATURE 120

int32_t pootbus_master_init();
int32_t pootbus_read_temperature(uint8_t slave_address);
void pootbus_calc_temperatures();
void pootbus_request_data();
void pootbus_reset();
int32_t pootbus_check_for_timeout();
int32_t pootbus_check_motor_temperatures();
int32_t pootbus_get_motor_temperature_fp3(int32_t index);


#endif /* __POOTBUS_H__ */
