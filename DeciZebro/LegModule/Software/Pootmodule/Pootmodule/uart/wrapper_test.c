/*!
 *  \file    wrapper_test.c
 *  \author  Wim Dolman (<a href="email:w.e.dolman@hva.nl">w.e.dolman@hva.nl</a>)
 *  \date    29-11-2013
 *  \version 1.1
 *
 *  \brief   Example for wrapper (uart.c and uart.h).
 *
 *  \details This example using the wrapper (uart.c and uart.h)
 *           for the UART-driver from Atmel's application note AVR1307
 *           (usart_driver.c and usart_driver.h)
 *           which uses avr_compiler.h.
 *
 *           This example uses the wrapper to receive a byte
 *           and to send this byte back in a formatted text string.
 *
 *           \note With the internal RC-oscillators 2 MHz or 32 MHz, it can be
 *           necessary to calibrate this internal clock.
 */
#define F_CPU     2000000UL       //!< system clock frequency

#include <avr/io.h>
#include <avr/interrupt.h>

/*!
 * \brief Macro ENABLE_UART_C1 non zero, in order to ensure
 *        that UART C1 is used.
 */
#define ENABLE_UART_C1   1
#define C1_BAUD          115200    //!< baud rate
#define C1_CLK2X         0         //!< no double clock speed
#include "uart.h"

/*! \brief main routine
 *
 *  It initializes the USARTC1 and receive characters from the
 *  UART and sends the characters back in a formatted text string.
 *
 *  \return int
 */
int main(void)
{
  uint16_t c;

  init_uart(&uartC1, &USARTC1, F_CPU, C1_BAUD, C1_CLK2X);

  PMIC.CTRL = PMIC_LOLVLEN_bm;
  sei();

  while(1) {
    if ( (c = uart_getc(&uartC1)) == UART_NO_DATA) {
      continue;
    }

    uart_puts(&uartC1, "Character: '");
    uart_putc(&uartC1, c);
    uart_puts(&uartC1, "'\n");
  }
}
