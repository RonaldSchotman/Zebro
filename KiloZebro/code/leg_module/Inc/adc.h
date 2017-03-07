/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: adc.h
 *
 * Description:
 * Code to drive the ADC
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#include "stdint.h"

#ifndef __ADC_H__
#define __ADC_H__

int32_t adc_init();
void adc_write_data_to_vregs();
void adc_request_conversion(void);
void adc_wait_for_data(void);
int32_t adc_get_temperature(void);
int32_t adc_get_absolute_motor_current(void);
int32_t adc_check_motor_current(void);
uint16_t adc_get_value(int32_t index);


/* Temperature sensor calibration value address */
//#define ADC_TEMP_AVG_SLOPE_FP3 ((int32_t) 4)
//#define ADC_VDD_FP6 ((int32_t) 3300)
//#define ADC_TEMP30_CAL_ADDR ((uint16_t*) ((uint32_t) 0x1FFFF7B8))
#define ADC_TEMP30_VOLTAGE_FP3 1430

/* Temperature sensor calibration value address */
//#define TEMP110_CAL_ADDR ((uint16_t*) ((uint32_t) 0x1FFFF7C2))
#define TEMP110_CAL_ADDR 557 // calculated using TEMP30 (printed on screen: 213) and an average slope of 4.3 and rounded. (4.3*80+213 = 557)
#define TEMP30_CAL_ADDR ((uint16_t*) ((uint32_t) 0x1FFFF7B8))
#define VDD_CALIB ((uint16_t) (330))
#define VDD_APPLI ((uint16_t) (300))

#define ADC_FULL_RANGE_COUNT 4096
#define ADC_MID_RANGE_COUNT 2048
#define ADC_FULL_RANGE_MILLIVOLT 3300
#define ADC_MID_RANGE_MILLIVOLT 1650

#define ADC_CURRENT_SENSITIVITY 55 // mV/A
#define ADC_CURRENT_EMERGENCY_VALUE 24000 // mA
#define ADC_CURRENT_EMERGENCY_SAMPLES 100

#define ADC_HAL_1_PIN 0
#define ADC_HAL_1_BANK GPIOC
#define ADC_HAL_2_PIN 1
#define ADC_HAL_2_BANK GPIOC
#define ADC_HAL_3_PIN 2
#define ADC_HAL_3_BANK GPIOC
#define ADC_ID_RESISTOR_PIN 3
#define ADC_ID_RESISTOR_BANK GPIOC
#define ADC_BATTERY_PIN 4
#define ADC_BATTERY_BANK GPIOC
#define ADC_MOTOR_CURRENT_PIN 5
#define ADC_MOTOR_CURRENT_BANK GPIOC

#define ADC_NUM_OF_CHANNELS 7

#define ADC_HAL_1_CH 10
#define ADC_HAL_2_CH 11
#define ADC_HAL_3_CH 12
#define ADC_ID_RESISTOR_CH 13
#define ADC_BATTERY_CH 14
#define ADC_MOTOR_CURRENT_CH 15
#define ADC_TEMP_CH 16

#define ADC_HAL_1_INDEX 0
#define ADC_HAL_2_INDEX 1
#define ADC_HAL_3_INDEX 2
#define ADC_ID_RESISTOR_INDEX 3
#define ADC_BATTERY_INDEX 4
#define ADC_MOTOR_CURRENT_INDEX 5
#define ADC_TEMP_INDEX 6

#endif /* __ADC_H__ */
