/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: peak.h
 *
 * Description:
 * Detect the peaks in the data send from the hall sensors
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __PEAK_H__
#define __PEAK_H__

#define PEAK_ERROR -1
#define PEAK_NUM_OF_SENSORS 3
#define PEAK_HISTORY_LAG 8 //because we want to bitshift to perform division, this number should be 2, 4, 8 and so on. max 255

uint8_t peak_process_adc_values_sensor(void);
uint8_t peak_get_adc_channel_index(uint8_t sensor);
void move_over_array_elements (uint16_t *array, uint8_t array_size);
uint16_t mean (uint16_t *array, uint8_t array_size);
uint8_t get_peak_detected(uint8_t sensor);
void reset_peak_detected(void);


/* ------- OLD CODE ---------*/

//int32_t peak_process_adc_values(void);
//int8_t peak_write_debug_info(void);
//int32_t peak_update_maximum(uint8_t sensor, int32_t adc_data);
//int32_t peak_update_minimum(uint8_t sensor, int32_t adc_data);
//int32_t peak_check_for_direction_change(uint8_t sensor, int32_t adc_data);
//int32_t peak_check_for_valid_peak(uint8_t sensor);
//int32_t peak_check_for_equilibrium_change(uint8_t sensor);
//int32_t peak_get_median_value(uint8_t sensor, int32_t adc_data);
//void set_calibration_peak_detected_to_zero(void);
//#define PEAK_INDEX_PEAK_DETECTED 2 // not changed in current code
//#define PEAK_DEFAULT_EQUILIBRIUM  2150
//#define PEAK_STATE_IDLE 0
//#define PEAK_STATE_RISING 1
//#define PEAK_STATE_FALLING 2
//#define PEAK_NORMAL_PEAK_DETECTED 1
//#define PEAK_STATE_CHANGE_HYSTERESIS 150
//#define PEAK_MINIMUM_PEAK_HEIGHT 200
//#define PEAK_MAX_HISTORY_DIFF 50
//#define PEAK_EQUILIBRIUM_HISTORY_SIZE 4
#endif /* __PEAK_H__ */
