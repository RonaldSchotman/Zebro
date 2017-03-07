/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: uart1.h
 *
 * Description:
 * Code to drive UART1, used for debugging
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */
#include "stdint.h"

#ifndef __UART1_H__
#define __UART1_H__

#define UART1_BAUD_RATE
#define UART1_TX_PIN GPIO_PIN_6
#define UART1_TX_BANK GPIOB
#define UART1_RX_PIN GPIO_PIN_10
#define UART1_RX_BANK GPIOA

#define UART1_BAUD_RATE_DIVIDER 0x18


int32_t uart1_init(void);
int32_t uart1_send_raw(uint8_t tx_data);
int32_t uart1_init_dma(void);
int32_t uart1_trigger_dma_once(void);
int32_t uart1_wait_until_done(void);
int32_t uart1_pins_init(void);


#endif /* __UART1_H__ */
