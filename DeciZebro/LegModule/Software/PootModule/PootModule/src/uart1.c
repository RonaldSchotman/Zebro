/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: uart1.h
 *
 * Description:
 * Code to drive UARTD0, used for debugging
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms -- d.booms@solcon.nl
 */


#include "asf.h"
#include "../inc/uart1.h"
#include "../inc/leds.h"
#include "../inc/vregs.h"

uint8_t vregs[VREGS_FILE_TOTAL_SIZE];
uint8_t vregs_buffer[VREGS_NUM_OF_BUFFERS][VREGS_FILE_TOTAL_SIZE];



int8_t uart1_init(void){
	sysclk_enable_module(SYSCLK_PORT_D, SYSCLK_USART0);
	uart1_pins_init();
	/* Set baud rate to 115.2 kbaud */
	/*BSEL = 131, BSCALE = -3, see page 213 of the reference manual */
	USARTD0.BAUDCTRLA = 0x83; /* 131 */
	USARTD0.BAUDCTRLB = 0xD0; /* -3, upper 4 bits */	
	/* Set communication mode to UART */
	/* Set data frame length to 8-bit */
	/* Turn of Parity checks */
	USARTD0.CTRLC = USART_CMODE_ASYNCHRONOUS_gc | USART_PMODE_DISABLED_gc | USART_CHSIZE_8BIT_gc;
	/* Enable USART transmitter */
	USARTD0.CTRLB = USART_RXEN_bm | USART_TXEN_bm;
	
	return 0;
}

/**
 * Initialise the UART, and set it up for continuously transferring information
 * from the vregs over DMA.
 */
int8_t uart1_init_dma(void){

	/*
	 * FIRST set up the UART
	 * */
	uart1_pins_init();

	/* Enable USART transmitter */
	USARTD0_CTRLB |= USART_TXEN_bm;
	/* Set communication mode to UART */
	USARTD0_CTRLC |= USART_CMODE_ASYNCHRONOUS_gc;
	/* Set data frame length to 8-bit */
	USARTD0_CTRLC |= USART_CHSIZE_8BIT_gc;
	/* Set baud rate to 115.2 kbaud */
	/*BSEL = 131, BSCALE = -3, see page 213 of the reference manual */
	USARTD0_BAUDCTRLA |= 0x83; /* 131 */
	USARTD0_BAUDCTRLB |= (0b1101<<4); /* -3 */
	

	/*
	 * SECOND set up the DMA channel
	 * DMA channel 3 is used for UART
	 * The block is the 256 bytes of the VREG, 
	 * The block consists of bursts of 1 byte
	 * */
	
	/* Send clk to DMA controller */
	sysclk_enable_module(SYSCLK_PORT_D, SYSCLK_DMA);
	/* Enable DMA controller, leave further settings at default*/
	DMA_CTRL |= DMA_ENABLE_bm;
	
	/* Reload start address after each block transfer */
	DMA_CH3_ADDRCTRL |= DMA_CH_SRCRELOAD_BLOCK_gc;
	/* Increment address after each burst */
	DMA_CH3_ADDRCTRL |= DMA_CH_SRCDIR_INC_gc;
	/* Do not alter destination address, leave reload setting at default: none*/
	DMA_CH3_ADDRCTRL |= DMA_CH_DESTDIR_FIXED_gc;
	/* Turn trigger for DMA off, use only software triggers*/
	/* Set UART as trigger for DMA to run continuously*/
	DMA_CH3_TRIGSRC = 0x00;
	//DMA_CH3_TRIGSRC = UART1_TRIGGER_ADDRESS;
	/* Set transfer count in bytes to size of VREGS */
	DMA_CH3_TRFCNT	= VREGS_FILE_TOTAL_SIZE;
	/* Set repeat count to unlimited */
	DMA_CH3_REPCNT = 0;
	/* Read the data from the VREGS */
	DMA_CH3_SRCADDR0 =  (uint8_t) vregs_get_buffer_address();
	/* And write it to the UART */
	DMA_CH3_DESTADDR0 = (uint8_t) &USARTD0_DATA;
	/* Set repeat mode, do not set singe shot mode if you want to trigger in software
	 * Do set singe shot mode when you want to continuously tranfer*/
	//DMA_CH3_CTRLA |= DMA_CH_SINGLE_bm;
	DMA_CH3_CTRLA |= DMA_CH_REPEAT_bm;
		
	/*
	 * THIRD enable the DMA channel
	 */
	DMA_CH3_CTRLA |= DMA_ENABLE_bm;

	return 0;
}

/**
 * Wait for the last UART data dump to be finished
 */
int8_t uart1_wait_until_done(void){
	/* wait until the DMA says the transfer is done */
	while(!(DMA_CH3_CTRLB & DMA_CH_CHBUSY_bm));
	/* we don't reset the flag here, because that is done in
	 * uart1_trigger_dma_once() */

	return 0;
}



/**
 * Write the correct data to the vregs, and transmit it over the UART
 */
int8_t uart1_trigger_dma_once(void){
	/* if the transfer is done */
	if(DMA_CH3_CTRLB & DMA_CH_CHBUSY_bm){
		/* copy the right data in to the vreg data buffer */
		vregs_writeout();
		/* clear the flag */
		DMA_CH3_CTRLB |= DMA_CH_TRNIF_bm;
		/* enable the channel */
		DMA_CH3_CTRLA |= DMA_ENABLE_bm;
		/* Request transfer */
		DMA_CH3_CTRLA |= DMA_CH_TRFREQ_bm;
	}

	return 0;
}

/**
 * Configures the pins corresponding to USARTD0
 */
int8_t uart1_pins_init(void){
	/* Configure TX pin as output, RX as input*/
	UART1_TX_PORT.DIRCLR = UART1_TX_PIN;
	UART1_TX_PORT.OUTSET = UART1_TX_PIN;
	UART1_TX_PORT.DIRSET = UART1_TX_PIN;
	UART1_RX_PORT.DIRCLR = UART1_RX_PIN;
	UART1_RX_PORT.PIN2CTRL = PORT_OPC_PULLUP_gc;


	return 0;
}

/**
 * Send out a raw byte over USART
 * This function uses busy waits
 * This function is used for debug purposes
 */
int8_t uart1_send_raw(uint8_t tx_data){
	/* wait for transmit data register to be empty */
	leds_set_LD1();
	while(!(USARTD0.STATUS & USART_DREIF_bm)){}
	leds_clear_LD1();
	/* clear flag */
	USARTD0.STATUS |= USART_TXCIF_bm;
	/* place new data in transmit data register */
	USARTD0.DATA = tx_data;
	//USARTD0.CTRLB |= USART_TXEN_bm;

	return 0;
}
