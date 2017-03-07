/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: uart1.c
 *
 * Description:
 * Code to drive UART1, used for debugging
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#include "stm32f0xx_hal.h"
#include "stdint.h"

#include "uart1.h"
#include "leds.h"
#include "stdint.h"
#include "vregs.h"

uint8_t vregs[VREGS_FILE_TOTAL_SIZE];
uint8_t vregs_buffer[VREGS_NUM_OF_BUFFERS][VREGS_FILE_TOTAL_SIZE];



int32_t uart1_init(void){
	uart1_pins_init();

	__HAL_RCC_USART1_CLK_ENABLE();

	/* keep many of the default settings, oversampling, word length ... */
	/* set baud rate to 115.2 kbaud */
	USART1->BRR = UART1_BAUD_RATE_DIVIDER;
	/* enable the UART transmitter*/
	USART1->CR1 |= USART_CR1_TE | USART_CR1_UE;

	return 0;
}

/**
 * Initialise the UART, and set it up for continuously transferring information
 * from the vregs over DMA.
 */
int32_t uart1_init_dma(void){

	/*
	 * FIRST set up the UART
	 * */
	uart1_pins_init();

	__HAL_RCC_USART1_CLK_ENABLE();

	/* keep many of the default settings, oversampling, word length ... */
	/* set baud rate to 115.2 kbaud */
	USART1->BRR = UART1_BAUD_RATE_DIVIDER;
	/* set DMA transmitter mode */
	USART1->CR3 |= USART_CR3_DMAT;

	/* enable the UART transmitter*/
	USART1->CR1 |= USART_CR1_TE | USART_CR1_UE;

	/*
	 * SECOND set up the DMA channel
	 * DMA channel 4 is used for UART1
	 * */

	__HAL_RCC_DMA1_CLK_ENABLE();

	/* map the USART1_TX DMA request to the correct DMA channel */
	SYSCFG->CFGR1 |=  SYSCFG_CFGR1_USART1TX_DMA_RMP;

	/* channel has low priority, 8-bit memory size, 8 bit peripheral size */
	DMA1_Channel4->CCR |= DMA_CCR_MINC;
	/* set circular mode */
	//DMA1_Channel4->CCR |= DMA_CCR_CIRC;
	/* read data from memory, write to peripheral */
	DMA1_Channel4->CCR |= DMA_CCR_DIR;
	/* we want to transfer the entire vregs virtual register file */
	DMA1_Channel4->CNDTR = VREGS_FILE_TOTAL_SIZE;
	/* write the data to the USART.TDR register */
	DMA1_Channel4->CPAR = (uint32_t) &(USART1->TDR);
	/* and read from the vregs virtual register file */
	DMA1_Channel4->CMAR = (uint32_t) vregs_get_buffer_address();

	/*
	 * THIRD clear the TC flag, and enable the DMA channel
	 */
	USART1->ICR |= USART_ICR_TCCF;
	DMA1_Channel4->CCR |= DMA_CCR_EN;

	return 0;
}

/**
 * Wait for the last UART data dump to be finished
 */
int32_t uart1_wait_until_done(void){
	/* wait until the DMA says the transfer is done */
	while(!(DMA1->ISR & DMA_ISR_TCIF4));
	/* we don't reset the flag here, because that is done in
	 * uart1_trigger_dma_once() */

	return 0;
}



/**
 * Write the correct data to the vregs, and transmit it over the UART
 */
int32_t uart1_trigger_dma_once(void){
	/* if the transfer is done */
	if(DMA1->ISR & DMA_ISR_TCIF4){
		/* copy the right data in to the vreg data buffer */
		vregs_writeout();
		/* clear the flag */
		DMA1->IFCR |= DMA_IFCR_CTCIF4;
		/* disable the channel */
		DMA1_Channel4->CCR &= ~DMA_CCR_EN;
		/* set the origin of the data */
		DMA1_Channel4->CMAR = (uint32_t) vregs_get_buffer_address();
		/* set the number of bytes to be transfered */
		DMA1_Channel4->CNDTR = VREGS_FILE_TOTAL_SIZE;
		/* enable the channel: send the data */
		DMA1_Channel4->CCR |= DMA_CCR_EN;
	}

	return 0;
}

/**
 * Configures the pins corresponding to UART1
 */
int32_t uart1_pins_init(void){
	GPIO_InitTypeDef  GPIO_InitStruct;

	/* enable UART1 GPIO clocks */
	__HAL_RCC_GPIOA_CLK_ENABLE();
	__HAL_RCC_GPIOB_CLK_ENABLE();

	/* set the GPIO pins */
	GPIO_InitStruct.Mode  = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull  = GPIO_PULLUP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;

	GPIO_InitStruct.Alternate = GPIO_AF0_USART1;
	GPIO_InitStruct.Pin = UART1_TX_PIN;
	HAL_GPIO_Init(UART1_TX_BANK, &GPIO_InitStruct);

	GPIO_InitStruct.Alternate = GPIO_AF0_USART1;
	GPIO_InitStruct.Pin = GPIO_PIN_6;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

	GPIO_InitStruct.Alternate = GPIO_AF1_USART1;
	GPIO_InitStruct.Pin = UART1_RX_PIN;
	HAL_GPIO_Init(UART1_RX_BANK, &GPIO_InitStruct);

	return 0;
}

/**
 * Send out a raw byte over UART1
 * This function uses busy waits
 */
int32_t uart1_send_raw(uint8_t tx_data){
	/* wait for transmit data register to be empty */
	while(!(USART1->ISR & USART_ISR_TXE));

	/* place new data in transmit data register */
	USART1->TDR = tx_data;

	return 0;
}
