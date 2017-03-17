/*
 * UART_portD.c
 *
 * Ring buffer Uart connected to port D. 
 *
 * Created: 07/12/2016 10:33:57
 *  Author: Eric Smit
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <stdbool.h>
#include <string.h>

#include "UART_portD.h"
#include "LightweightRingBuff.h"

// UART connection uses UART D0
#define  UART						USARTD0
#define  UART_RX_Vect				USARTD0_RXC_vect
#define  UART_DRE_Vect				USARTD0_DRE_vect
#define  UART_TXC_Vect				USARTD0_TXC_vect
//#define  UART_SYSCLK				SYSCLK_USART0
#define  UART_PORT					PORTD
#define  UART_PORT_PIN_TX			(1<<3)  // PD3 (TXDD0)
#define  UART_PORT_PIN_RX			(1<<2)  // PD2 (RXDD0)
//#define  UART_PORT_SYSCLK			SYSCLK_PORT_E
#define  UART_IO_RXDPIN_Vect		PORTD_INT0_vect

RingBuff_t data_transmit;
RingBuff_t data_receive;

#define UART_enableTransmit		UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_DREINTLVL_HI_gc | (register8_t) USART_TXCINTLVL_HI_gc) ) | (register8_t) USART_DREINTLVL_HI_gc | (register8_t) USART_TXCINTLVL_HI_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_disableTransmit	UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_DREINTLVL_HI_gc | (register8_t) USART_TXCINTLVL_HI_gc) ) | (register8_t) USART_DREINTLVL_OFF_gc | (register8_t) USART_TXCINTLVL_OFF_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_enableDATAEMPTY	UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_DREINTLVL_HI_gc)) | (register8_t) USART_DREINTLVL_HI_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_disableDATAEMPTY	UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_DREINTLVL_HI_gc)) | (register8_t) USART_DREINTLVL_OFF_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_enableTRMCOMPL		UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_TXCINTLVL_HI_gc)) | (register8_t) USART_TXCINTLVL_HI_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_disableTRMCOMPL	UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_TXCINTLVL_HI_gc)) | (register8_t) USART_TXCINTLVL_OFF_gc ) // USART_DREINTLVL_HI_gc used as mask function
#define UART_enableReceive		UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_RXCINTLVL_HI_gc)) | (register8_t) USART_RXCINTLVL_HI_gc ) // USART_RXCINTLVL_HI_gc used as mask function
#define UART_disableReceive		UART.CTRLA = ( (UART.CTRLA & ~((register8_t) USART_RXCINTLVL_HI_gc)) | (register8_t) USART_RXCINTLVL_OFF_gc ) // USART_RXCINTLVL_HI_gc used as mask function

volatile bool transmit_ongoing; 
volatile bool receive_ongoing;
volatile bool receive_timeout;

void uart_init(void)
{
	// uart initialization

	//set pins
 	UART_PORT.DIRCLR = UART_PORT_PIN_TX; // TX as input, is set as output when transmission starts.
	UART_PORT.DIRCLR = UART_PORT_PIN_RX; // RX as input.

	PORTD.DIRCLR = (1<<3); // TX as input, is set as output when transmission starts.
	PORTD.OUTSET = (1<<3);
	
	PORTD.PIN2CTRL = PORT_OPC_PULLUP_gc;
	PORTD.DIRCLR = (1<<2);


	// Set configuration
	UART.CTRLC = USART_CMODE_ASYNCHRONOUS_gc | USART_PMODE_DISABLED_gc | USART_CHSIZE_8BIT_gc;

	// Update baud rate
	//	baudrate = 115200 @ 32MHz 
	// Baud select = 131 => 0x083 (12 bits, 8 least significant are reg BAUDCTRLA, others are the botom 4 of BAUDCTRLB)
	// scaler = -3 => 0xD (4 bits, the top four of BAUDCTRLB
// 	UART.BAUDCTRLA = 0x83;
// 	UART.BAUDCTRLB = 0xD0;
	
	// baudrate = 19200 @32MHz
	// baudsect = 12 => 0x00C
	// scaler = 3 => 0x3
	UART.BAUDCTRLA = 0x0C;
	UART.BAUDCTRLB = 0x30;
	
	// timer 1 configuration, this timer is used to reset the protocol handler if time between bytes is to long
	// configure timer to provide overflow interrupt, 
	TCD1.INTCTRLA = TC_TC1_OVFINTLVL_HI_gc;
	TCD1.PER = 32000; // a 1 ms overflow, this allows 19200 baud rate. 
	TCD1.CNT = 0;
	
//	TCD1.CTRLA = TC_TC0_CLKSEL_DIV1_gc; // turns the counter on.
	

	
	RingBuffer_InitBuffer(&data_receive);
	RingBuffer_InitBuffer(&data_transmit);

	UART.CTRLB = USART_RXEN_bm | USART_TXEN_bm;
 	UART.CTRLA = (register8_t) USART_RXCINTLVL_OFF_gc | (register8_t) USART_DREINTLVL_OFF_gc | (register8_t) USART_TXCINTLVL_OFF_gc;

	transmit_ongoing = false;
	receive_ongoing = false;
	receive_timeout = false;
	
	// initialize RXD pin interrupt.
	// set RXD pin to sense falling edges only.
	// interrupt enabling will be done in debug_proccess
	UART_PORT.INT0MASK |= UART_PORT_PIN_RX;
	UART_PORT.PIN2CTRL |= PORT_ISC_FALLING_gc;
	UART_PORT.INTCTRL = PORT_INT0LVL_HI_gc;
}

// function used By the protocol handler to tel the UART driver there is no more data to be received. 
void UART_receive_complete (void) 
{
	receive_ongoing = false;
	// enable pin interrupt / disable RX
	UART_PORT.INTFLAGS = PORT_INT0IF_bm;
	UART_PORT.INTCTRL = PORT_INT0LVL_HI_gc;
	UART_disableReceive;
	// turn timer counter off
	TCD1.CTRLA = TC_TC0_CLKSEL_OFF_gc; // turns the counter on.
	TCD1.CNT = 0;
}

// UART sleep mode returns if UART is working and the sleep mode needs to be decreased.
// return 1 if UART active
// return 0 if UART is inactive
bool UART_sleep_mode (void)
{
	return (transmit_ongoing | receive_ongoing);
}

uint8_t UART_Receive( void )
{
	if (!RingBuffer_IsEmpty(&data_receive))
	{
		return RingBuffer_Remove(&data_receive);
	}
	return 0;
}

void UART_Transmit( uint8_t data )
{
	if (!RingBuffer_IsFull(&data_transmit))
	{
		RingBuffer_Insert(&data_transmit, data);
	}
	UART_PORT.DIRSET = UART_PORT_PIN_TX; // TX as output.
	USARTD0.STATUS = USART_TXCIF_bm;
	UART_enableTransmit;
	transmit_ongoing = true;
}

bool UART_DataReady( void )
{
	return !RingBuffer_IsEmpty(&data_receive);
}

// sending strings
uint8_t UART_Send_FlashStr( const char * str )
{
	uint8_t count = 0;								// Initialize byte counter

	while ( pgm_read_byte(&(*str)) != 0 )			// Reached zero byte ?
	{
		UART_Transmit(pgm_read_byte(&(*str++ )));   // Send character and increment pointer
		count++;									// Increment byte counter
	}
	return count;									// Return byte count
}

uint8_t UART_Send_RAMStr( char * str )
{
	uint8_t count = 0;            // Initialize byte counter

	while( *str != 0 )                  // Reached zero byte ?
	{
		UART_Transmit( *str++ );						// Send character and increment pointer
		count++;                        // Increment byte counter
	}
	return count;                       // Return byte count
}

bool UART_Receive_timeout(void)
{
	return receive_timeout;
}

void UART_Receive_timeout_clear(void)
{
	receive_timeout = false;
}

// interrupt functions

//Transmission data register empty register
ISR(UART_DRE_Vect)
{
	// Check if all data is transmitted 
	if ( !RingBuffer_IsEmpty(&data_transmit) )
	{
		UART.DATA = RingBuffer_Remove(&data_transmit);  // Start transmission
	}
	else
	{
		UART_disableDATAEMPTY;
		USARTD0.STATUS = USART_TXCIF_bm;
	}
}

ISR(USARTD0_TXC_vect)
{
	// if this is handled the transmission is complete 	
	UART_disableTransmit;
	transmit_ongoing = false;
	UART_PORT.DIRCLR = UART_PORT_PIN_TX; // TX as input.
}

//Receive interrupt
ISR(USARTD0_RXC_vect)
{
	if (!RingBuffer_IsFull(&data_receive))
	{
		RingBuffer_Insert(&data_receive, UART.DATA);
	}
	// reset and enabel timeout counter
	TCD1.CNT = 0;
	TCD1.CTRLA = TC_TC0_CLKSEL_DIV1_gc; // turns the counter on.
}

// On port D only the RX pin uses pin change interrupt. 
// RX pin change interrupt is used to allow power save sleep mode operation. 
ISR(UART_IO_RXDPIN_Vect)
{
	receive_ongoing = true;

	// disable pin interrupt / enable uart RX
	UART_PORT.INTCTRL = PORT_INT0LVL_OFF_gc;
	UART_enableReceive;
	// reset and enabel timeout counter
	TCD1.CNT = 0;
	TCD1.CTRLA = TC_TC0_CLKSEL_DIV1_gc; // turns the counter on.
}

ISR(TCD1_OVF_vect)
{
	// timeout occurred. turn uart receive off. 
	TCD1.CTRLA = TC_TC0_CLKSEL_OFF_gc; // turns the counter on.
	TCD1.CNT = 0;
	
	receive_timeout = true;
	receive_ongoing = false;
	// enable pin interrupt / disable RX
	UART_PORT.INTFLAGS = PORT_INT0IF_bm;
	UART_PORT.INTCTRL = PORT_INT0LVL_HI_gc;
	UART_disableReceive;
}
