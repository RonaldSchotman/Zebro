/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: uart1.h
 *
 * Description:
 * Code to drive UART1, used for debugging
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms -- d.booms@solcon.nl
 */

#ifndef __UART1_H__
#define __UART1_H__

#define UART1_BAUD_RATE
#define UART1_TX_PIN		PIN3_bm
#define UART1_TX_PORT		PORTD
#define UART1_RX_PIN		PIN2_bm
#define UART1_RX_PORT		PORTD

#define UART1_BAUD_RATE_DIVIDER		0x18

#define UART1_DATA_REGISTER_ADDRESS 0x4B
#define UART1_TRIGGER_ADDRESS		0x4C



int8_t uart1_init(void);
int8_t uart1_send_raw(uint8_t tx_data);
int8_t uart1_init_dma(void);
int8_t uart1_trigger_dma_once(void);
int8_t uart1_wait_until_done(void);
int8_t uart1_pins_init(void);


#endif /* __UART1_H__ */
