/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: leds.c
 *
 * Description:
 * Code to drive the LEDs
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#include "stm32f0xx_hal.h"
#include "leds.h"

/**
 * initialise the GPIO ports for the leds on the discovery board
 * */
void leds_init(){
	GPIO_InitTypeDef GPIO_InitStruct;

	  /* GPIO Ports Clock Enable */
	__HAL_RCC_GPIOC_CLK_ENABLE();

	/* set up the pins as outputs */
	GPIO_InitStruct.Pin = LD3_PIN|LD4_PIN;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

	HAL_GPIO_Init(LD3_BANK, &GPIO_InitStruct);
}

/**
 * Function to set LD3 of the Discovery board.
 * Used for debugging
 */
void leds_set_LD3(){
	HAL_GPIO_WritePin(LD3_BANK, LD3_PIN, GPIO_PIN_SET);
}

/**
 * Function to clear LD3 of the Discovery board.
 * Used for debugging
 */
void leds_clear_LD3(){
	HAL_GPIO_WritePin(LD3_BANK, LD3_PIN, GPIO_PIN_RESET);
}

/**
 * Function to toggle LD3 of the Discovery board.
 * Used for debugging
 */
void leds_toggle_LD3(){
	  HAL_GPIO_TogglePin(LD3_BANK, LD3_PIN);
}

/**
 * Function used to let LD3 blink.
 * Will block the entire MCU, should only be used for debugging
 */
void leds_blink_LD3_blocking(){
	while(1){
		leds_toggle_LD3();
		HAL_Delay(LEDS_H_BLINK_SPEED);
	}
}

/**
 * Function to set LD4 of the Discovery board.
 * Used for debugging
 */
void leds_set_LD4(){
	HAL_GPIO_WritePin(LD4_BANK, LD4_PIN, GPIO_PIN_SET);
}

/**
 * Function to clear LD4 of the Discovery board.
 * Used for debugging
 */
void leds_clear_LD4(){
	HAL_GPIO_WritePin(LD4_BANK, LD4_PIN, GPIO_PIN_RESET);
}

/**
 * Function to toggle LD4 of the Discovery board.
 * Used for debugging
 */
void leds_toggle_LD4(){
	HAL_GPIO_TogglePin(LD4_BANK, LD4_PIN);
}

/**
 * Function used to let LD4 blink.
 * Will block the entire MCU, should only be used for debugging
 */
void leds_blink_LD4_blocking(){
	while(1){
		leds_toggle_LD4();
		HAL_Delay(LEDS_H_BLINK_SPEED);
	}
}
