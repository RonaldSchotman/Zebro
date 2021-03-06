/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: main.c
 *
 * Description:
 * main C file for the Zebro POOT leg module.
 * This file is part of a bachelor graduation project
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms -- d.booms@solcon.nl
 */

#include "stdint.h"

#include "stm32f0xx_hal.h"

#include "globals.h"
#include "leds.h"
#include "adc.h"
#include "uart1.h"
#include "vregs.h"
#include "pootbus.h"
#include "zebrobus.h"
#include "h_bridge.h"
#include "time.h"
#include "errors.h"
#include "motion.h"
#include "fans.h"
#include "address.h"
#include "interrupts.h"
//#include "peak_detect.h"
#include "peak.h"
//#include "position.h"
//#include "walk.h"
//#include "sequencer.h"
#include "encoder.h"

void SystemClock_Config(void);

int main(void) {
	/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
	HAL_Init();

	/* Configure the system clock */
	SystemClock_Config();

	/* initialise all the things */
	uart1_init_dma();
	h_bridge_init();
	/* ADC is coupled with TIM1_CC4 in h_bridge_init() */
	adc_init();
	vregs_init();
	errors_init();
	leds_init();
	time_init();
	fans_init();
	encoder_init();
	/* need to get ADC data before running address_init() */
	address_init();
	/* zebrobus uses address */
	zebrobus_slave_init();
	/* motion uses zebrobus, encoder */
	motion_init();
	pootbus_master_init();

	/* keep a loop counter */
	uint8_t loop_counter = 0;
	uint32_t start_time, stop_time = 0;

	/* check why we had a reset */
	vregs_write(VREGS_RCC_CSR31_24, RCC->CSR >> 24);
	vregs_write(VREGS_RCC_CSR23_16, RCC->CSR >> 16);
	RCC->CSR |= RCC_CSR_RMVF;

	while (1) {
		start_time = time17_get_time();
		//todo: implement system where motor will stop executing a command
		// when no drive command have been received for a number of seconds

		/**
		 * This is the main loop.
		 * Every time new measurement data is available we go through it
		 */
		address_write_to_vregs();

		/* trigger PootBus if needed */
		pootbus_request_data();
		/* process data from PootBus */
		pootbus_check_motor_temperatures();

		/* let the watchdog now we are still alive */
		time_reset_watchdog();

		/* process data from ADC */
		adc_write_data_to_vregs(); /* not the most recent data, maybe, but that's not important */
		adc_check_battery_voltage();
		adc_get_temperature();
		fans_calc_and_set_speeds();

		/* process commands from ZebroBus */
		zebrobus_process_write_requests();

		/* Things in here for temporary debug */
		time_check_time();
//		time_dumy_locmotive_controller();

		encoder_write_to_vregs();
		motion_absolute_position_calculator();
		motion_command_zebro();

		/* waiting until the previous uart transfer is done can be very useful
		 * during debugging. It ensures that you have information about
		 * every iteration of the loop in the debug log. When I (Piet) wrote this,
		 * this lowers the loop frequency by a factor 4 */
//		uart1_wait_until_done();

		/* send out the current state of the data over the UART,
		 * In this function we also swap the vregs buffers. Thus,
		 * the vregs buffer is only updated every time the data dump
		 * over the UART is done.
		 */
		uart1_trigger_dma_once();

		/* count, count, count */
		vregs_write(VREGS_LOOP_COUNTER, loop_counter++);

		stop_time = time17_get_time();
		uint32_t time_diff = stop_time - start_time; /* automatically deals with rollover because of uint */
		time_diff = time_diff / 48; /* convert to us */
		vregs_write(VREGS_LOOP_TIME, (uint8_t) time_diff);
	}

	/* this should never happen */
	leds_blink_LD3_blocking();

}

/** System Clock Configuration
 */
void SystemClock_Config(void) {

	RCC_OscInitTypeDef RCC_OscInitStruct;
	RCC_ClkInitTypeDef RCC_ClkInitStruct;
	RCC_PeriphCLKInitTypeDef PeriphClkInit;

	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI
			| RCC_OSCILLATORTYPE_HSI14;
	RCC_OscInitStruct.HSIState = RCC_HSI_ON;
	RCC_OscInitStruct.HSI14State = RCC_HSI14_ON;
	RCC_OscInitStruct.HSICalibrationValue = 16;
	RCC_OscInitStruct.HSI14CalibrationValue = 16;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
	RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
	RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL12;
	RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
	HAL_RCC_OscConfig(&RCC_OscInitStruct);

	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
			| RCC_CLOCKTYPE_PCLK1;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
	HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1);

	PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1
			| RCC_PERIPHCLK_I2C1;
	PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK1;
	PeriphClkInit.I2c1ClockSelection = RCC_I2C1CLKSOURCE_HSI;
	HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit);

	HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq() / 1000);

	HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
	/* SysTick_IRQn interrupt configuration */
	//HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
	HAL_NVIC_SetPriority(-1, 0, 0);
}

#ifdef USE_FULL_ASSERT

/**
 * @brief Reports the name of the source file and the source line number
 * where the assert_param error has occurred.
 * @param file: pointer to the source file name
 * @param line: assert_param error line source number
 * @retval None
 */
void assert_failed(uint8_t* file, uint32_t line)
{
	/* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
	 ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
	/* USER CODE END 6 */

}

#endif
