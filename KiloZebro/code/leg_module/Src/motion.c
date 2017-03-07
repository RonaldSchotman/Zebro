/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: motion.c
 *
 * Description:
 * Motion controller. Keeps track of the current walking
 * mode or assignment, and decides how to actuate the
 * H-bridge.
 * *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 *
 * Last edited:
 * 06-03-2017		Floris Rouwen		florisrouwen@outlook.com
 */

#include "stdint.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "motion.h"
#include "vregs.h"
#include "h_bridge.h"
#include "address.h"
#include "time.h"
#include "encoder.h"
#include "peak.h"
#include "adc.h"

static struct motion_state state = { 0, 0, 0, 0, 0 };
static struct motion_state new_state = { 0, 0, 0, 0, 0 };
uint32_t std_var; /* standard deviation of the hall-sensor with a peak at hall-sensor 3. */
uint16_t position_touch_down = 0;
uint8_t calibrate = 1; /* When Zebro is turned on, calibrate should first be on. */
static uint16_t touch_down_position = 0;
static uint16_t stand_up_position = 0;
static uint16_t lift_off_position = 0;
//static uint8_t next_walk_instruction;

/**
 * Process data send to any of the addresses in the motion control range.
 */
int32_t motion_new_zebrobus_data(uint32_t address, uint8_t data) {

	switch (address) {

	/* set mode */
	case VREGS_MOTION_MODE:
		new_state.mode = data;
		break;

		/* set speed */
	case VREGS_MOTION_SPEED:
		new_state.speed = data;
		break;

		/* set phase */
	case VREGS_MOTION_PHASE:
		new_state.phase = data;
		break;

		/* set extra */
	case VREGS_MOTION_EXTRA:
		new_state.extra = data;
		break;

		/* set crc */
	case VREGS_MOTION_CRC:
		new_state.crc = data;
		break;

		/* check if the new command is sane, and if it is, activate it.
		 * Reset the 'new_state' struct in either case
		 */
	case VREGS_MOTION_UPDATE:
		if (!motion_validate_state(new_state)) {
			state = new_state;
			motion_write_state_to_vregs(state);
		}
		new_state.mode = 0;
		new_state.speed = 0;
		new_state.phase = 0;
		new_state.extra = 0;
		new_state.crc = 0;
		break;

	default:
		break;

	}
	return 0;
}

/**
 * Write the values of the given state to the vregs
 */
int32_t motion_write_state_to_vregs(struct motion_state motion_state) {
	vregs_write(VREGS_MOTION_MODE, motion_state.mode);
	vregs_write(VREGS_MOTION_SPEED, (uint8_t) (motion_state.speed));
	vregs_write(VREGS_MOTION_PHASE, motion_state.phase);
	vregs_write(VREGS_MOTION_EXTRA, motion_state.extra);
	vregs_write(VREGS_MOTION_CRC, motion_state.crc);

	return 0;
}

/**
 * Stub for the state validator.
 * return zero is state is OK.
 */
int32_t motion_validate_state(struct motion_state motion_state) {
	return 0;
}

/**
 * Look at the drive command, the position data, and the time.
 * Use this data to choose how to actuate the h_bridge.
 *
 * Info:
 * Left leg : get_address_side = 0; walking forward = counterclockwise = h_bridge_drive(x, 0, x) : encoder_dir = 1 : encoder = counting down.
 *
 * The finite state machine toggled by fsm_flag is as follows. For each number of fsm_flag=
 * 		0: Set encoder in the middle of it's range.
 * 		1: Rotate the leg backwards until it touches the ground.
 * 		2: Rotate the leg forward and collect hall-sensor samples. Store these in an array.
 * 		3: Reset the peak_detected array.
 * 		4: Rotate the leg backward until the 3rd hall-sensor is found and set the encoder value to zero.
 * 		5: Calibration completed, calculate the arrival time for the leg to stand position.
 * 		6: Rotate the leg forward until the stand position is reached.
 * 		7:
 */
int32_t motion_drive_h_bridge() {
	int32_t return_value = 0;
	static uint16_t adc_data[ARRAY_SIZE];
	static uint8_t fsm_flag = 0;
	static uint16_t position[2] = { 0, 0 };
	static uint32_t stand_up_time = 0;
	static uint32_t touch_down_time = 0;
	static uint32_t lift_off_time = 0;
	static uint8_t direction = 0;

	vregs_write(VREGS_DEBUG_FLAG_1, (uint8_t) fsm_flag);

	switch (state.mode) {

	case MOTION_MODE_IDLE:
		fsm_flag = 0;
		h_bridge_disable();
		return 0;

	case MOTION_MODE_CALIBRATE:
		if (fsm_flag == 0) {
			/* Set calibrate to 1 to enable reading adc-data of the hall-sensors */
			set_calibrate(1);
			/* Set the encoder value somewhere in the middle of its range to prevent wrapping around immediately. */
			encoder_set_position_mid();
			fsm_flag = 1;
		}
		if (fsm_flag == 1) {
			h_bridge_drive_motor(25, !address_get_side(),
			H_BRIDGE_MODE_SIGN_MAGNITUDE);
			/* If the legs current position is smaller of equal to the last position, we are touching the ground.
			 * What if the leg keeps spinning? How to calibrate then, because of overflow encoder etc? */
			if ((position[!address_get_side()] <= position[address_get_side()])) { /* We will always enter this loop the first time the calibrate-loop runs because positions are initialized equal.*/
				start_timing_measurement();
				/* wait for position data */
				if (stop_and_return_timing_measurement(400)) {
					h_bridge_disable();
					fsm_flag = 2;
				}
			} else {
				/* If the position condition was not satisfied, reset timer. */
				reset_timing_measurement();
			}
		}
		if (fsm_flag == 2) {
			static uint16_t n = 0;
			h_bridge_drive_motor(25, address_get_side(),
			H_BRIDGE_MODE_SIGN_MAGNITUDE);
			if (time_get_time_ms() % 10 == 0) { /* We don't want to sample too often */
				adc_data[n] = adc_get_value(2); /* We're only interested in the value of the 3rd hall sensor */
				n = n + 1;
			}
			if (n >= ARRAY_SIZE) {
				n = ARRAY_SIZE - 1;
			}
			/* If the legs current position is larger of equal to the last position, we are touching the ground.
			 * What if the leg keeps spinning? How to calibrate then, because of overflow encoder etc? */
			if ((position[!address_get_side()] >= position[address_get_side()])) { /* Condition is different since we turn the other way */
				start_timing_measurement();
				/* wait for position data */
				if (stop_and_return_timing_measurement(400)) {
					h_bridge_disable();
					/* Calculate the standard deviation of the collected samples. */
#ifdef DEBUG_VREGS
					std_var = std_var_stable(adc_data, n);
					vregs_write(VREGS_MOTION_STD_DEV_A,
							(uint8_t) get_std_var());
					vregs_write(VREGS_MOTION_STD_DEV_B,
							(uint8_t) (get_std_var() >> 8));
#endif
					fsm_flag = 3;
				}
			} else {
				/* If the position condition was not satisfied, reset timer. */
				reset_timing_measurement();
			}
		}
		if (fsm_flag == 3) {
			reset_peak_detected();
			fsm_flag = 4;
		}
		if (fsm_flag == 4) {
			h_bridge_drive_motor(25, !address_get_side(),
			H_BRIDGE_MODE_SIGN_MAGNITUDE);
			if (get_peak_detected(2) == 1) {
				h_bridge_disable();
				encoder_reset_position();
				motion_stop();
				set_calibrate(0);
				/* Do we need to free the adc_data memory? We don't need this array after this. */
//				for (i = 0; i < (ARRAY_SIZE - 1); i++) {
//					free(&adc_data[i]);
//					adc_data[i] = 0;
//				}
			}
		}

		/* Last thing that should happen in this loop, get new encoder data. Slower is better since there is a higher chance of spotting the stopping of rotation. */
		if (time_get_time_ms() % 200 == 0) {
			position[0] = position[1];
			position[1] = encoder_get_position();
		}
		break;

	case MOTION_MODE_CONTINUOUS_ROTATION:
		/* Continuously rotate the leg forward at a 10th of the dutycycle */
		h_bridge_drive_motor(25, address_get_side(),
		H_BRIDGE_MODE_SIGN_MAGNITUDE);
		break;

	case MOTION_MODE_WALK:
		// if motion_move_to_point = 1, pak dan het volgende punt. Als geen volgende punt, neem dan the stand-position. Als je daarvoor achteruit moet draaien, dan moet dat.
		direction = state.extra;
		lift_off_time = state.speed * 1000;
		touch_down_time = state.phase * 1000;

		if (fsm_flag == 0) {
			fsm_flag = 8;
		}

		if (fsm_flag == 8) {
			fsm_flag = fsm_flag
					+ motion_move_to_point(lift_off_position, direction,
							lift_off_time);
		}
		if (fsm_flag == 9) {
			fsm_flag = fsm_flag
					+ motion_move_to_point(touch_down_position, direction,
							touch_down_time);
		}
		if (fsm_flag == 10) {
			motion_stop(); /* if we use this, we only get into this loop when there actually is data. But then the leg stays at the touch down position. */
		}
		break;

	case MOTION_MODE_STAND_UP:
		if (fsm_flag == 0) {
			fsm_flag = 5;
		}
		stand_up_time = state.speed * 1000;
		if (fsm_flag == 5) {
			fsm_flag = fsm_flag
					+ motion_move_to_point(stand_up_position,
					MOTION_DIRECTION_FORWARD, stand_up_time);
		}
		if (fsm_flag == 6) {
			stand_up_time = 0;
			motion_stop();
		}
		break;

//	case MOTION_DEBUG_COMMAND:
//    	if(state.extra){
//    		step_rotate_three_start();
//    		state.extra = 0;
//    	}
//    	else{
//    		if (step_rotate_three_update()){
//    			h_bridge_disable();
//    			motion_stop();
//    		}
//    	}
//		break;

	default:
		h_bridge_disable();
		return_value = 255;
	}
	motion_write_state_to_vregs(state);
	return return_value;
}

//void set_next_walk_instruction(uint8_t value) {
//	next_walk_instruction = value;
//	return;
//}

/* Function to move the leg to a certain position (touch down, stand, or lift) with a certain direction (forward or backward).
 * dir should be 0 for forward and 1 for backward. Arrival time should be in absolute milliseconds.
 *
 * Info:
 * Left leg : get_address_side = 0; walking forward = counterclockwise = h_bridge_drive(x, 0, x) : encoder_dir = 1 : encoder = counting down.
 */
uint8_t motion_move_to_point(uint16_t position, uint8_t dir,
		uint32_t arrival_time) {
	uint8_t status = 0; /* Turns 1 when the point was reached. */
	int32_t direction = address_get_side() ^ dir; /* Bitwise xor makes direction correct for any dir on any leg. */
	uint8_t dutycycle = 0;
	uint16_t difference_position = 0;
	uint32_t difference_time = 0;
	uint16_t current_position = encoder_get_position();

	/* Backward */
	if (dir) {
		/* Later on we will check if the time difference is large than zero. */
		difference_time = time_calculate_delta(arrival_time,
				time_get_time_ms());

		/* Calculate the number of pulses before we reach the correct position. */

		/* Left-side & past position already. */
		if (!address_get_side() && (current_position > position)) {
			difference_position = ((ENCODER_PULSES_PER_ROTATION
					- current_position) + position);
		}
		/* Left-side & didn't pass position yet */
		else if (!address_get_side() && (current_position < position)) {
			difference_position = position - current_position;
		}
		/* Right-side & past position already */
		else if (address_get_side() && current_position < position) {
			difference_position = (current_position + position);
		}
		/* Right-side & didn't pass position yet */
		else if (address_get_side() && current_position > position) {
			difference_position = current_position - position;
		} else {
			difference_position = 0; /* This is safe since dutycycle will be zero because of this. */
		}

		/* Calculate the dutycycle necessary to get the leg at the right position at the right time. */
		if (difference_time > 0) {
			dutycycle = (uint8_t) ((difference_position * 1000)
					/ (DUTYCYCLE_PER_PULSE_PER_SECOND * difference_time));
		} else {
			dutycycle = 0; /* We are not actually sending this value to the h-bridge, because that would be bad. */
		}
		/* Check if the leg arrived. */
		if (((current_position >= position)
				&& (current_position <= (position + MOTION_POSITION_HYSTERESIS))
				&& (!address_get_side()))
				|| ((current_position <= position)
						&& (current_position
								>= (position - MOTION_POSITION_HYSTERESIS))
						&& (address_get_side()))) {
//		if (current_position == position) { /* This works when checking at at least 1820 Hz since we want to guarantee functionality. */
			arrival_time = 0;
			status = 1;
		} else {
			if (dutycycle != 0) {
				h_bridge_drive_motor(dutycycle, direction,
				H_BRIDGE_MODE_SIGN_MAGNITUDE);
			} else {
				/* just keep turning. Don't really know if this is nice. We'll see. */
				h_bridge_drive_motor(25, direction,
				H_BRIDGE_MODE_SIGN_MAGNITUDE);
			}
		}
		/* Forward */
	} else {
		difference_time = time_calculate_delta(arrival_time,
				time_get_time_ms());

		/* Calculate the number of pulses before we reach the correct position. */

		/* Left-side & past position already. */
		if (!address_get_side() && (current_position < position)) {
			difference_position = (current_position + position);
		}
		/* Left-side & didn't pass position yet */
		else if (!address_get_side() && (current_position > position)) {
			difference_position = current_position - position;
		}
		/* Right-side & past position already */
		else if (address_get_side() && current_position < position) {
			difference_position = position - current_position;
		}
		/* Right-side & didn't pass position yet */
		else if (address_get_side() && current_position > position) {
			difference_position = (ENCODER_PULSES_PER_ROTATION
					- current_position) + position;
		} else {
			difference_position = 0; // This is safe since dutycycle will be zero because of this.
		}

		/* Calculate the dutycycle necessary to get the leg at the right position at the right time. */
		if (difference_time > 0) {
			dutycycle = (uint8_t) ((difference_position * 1000)
					/ (DUTYCYCLE_PER_PULSE_PER_SECOND * difference_time));
		} else {
			difference_time = 0;
			dutycycle = 0;
		}
		/* Check if the leg arrived. */
		if (((current_position <= position)
				&& (current_position >= (position - MOTION_POSITION_HYSTERESIS))
				&& (!address_get_side()))
				|| ((current_position >= position)
						&& (current_position
								<= (position + MOTION_POSITION_HYSTERESIS))
						&& (address_get_side()))) {
//		if (current_position == position) { /* This works when checking at at least 1820 Hz since we want to guarantee functionality. */
			arrival_time = 0;
			status = 1;
		} else {
			if (dutycycle != 0) {
				h_bridge_drive_motor(dutycycle, direction,
				H_BRIDGE_MODE_SIGN_MAGNITUDE);
			} else {
				/* just keep turning. Don't really know if this is nice. We'll see. */
				h_bridge_drive_motor(25, direction,
				H_BRIDGE_MODE_SIGN_MAGNITUDE);
			}
		}
	}
#ifdef DEBUG_VREGS
	vregs_write(VREGS_MOTION_ARRIVAL_TIME, (arrival_time >> 10));
	vregs_write(VREGS_MOTION_DUTYCYCLE, dutycycle);
	vregs_write(VREGS_MOTION_DELTA_T, difference_time >> 10);
	vregs_write(VREGS_MOTION_DELTA_S_A, difference_position);
	vregs_write(VREGS_MOTION_DELTA_S_B, difference_position >> 8);
#endif
	return status;
}

/* Return standard deviation */
uint32_t get_std_var(void) {
	return std_var;
}

/* Calculate the standard deviation from a vector with length n. */
uint16_t std_var_stable(uint16_t *a, uint16_t n) {
	if (n == 0)
		return 0;
	uint64_t sum = 0;
	uint64_t sq_sum = 0;
	unsigned i = 0;
	for (i = 0; i < n; ++i) {
		uint32_t ai = a[i];
		sum += ai;
		sq_sum += ai * ai; /*We lose accuracy, but it's okay*/
	}
	uint64_t N = n;
	uint32_t std_var = (N * sq_sum - sum * sum) / (N * N);
	std_var = (uint16_t) isqrt(std_var);
	return std_var;
}

/* Take the square root of x and round to the nearest integer. Copied from somewhere. */
uint32_t isqrt(uint32_t x) {
	register unsigned long op, res, one;

	op = x;
	res = 0;

	/* "one" starts at the highest power of four <= than the argument. */
	one = 1 << 30; /* second-to-top bit set */
	while (one > op)
		one >>= 2;

	while (one != 0) {
		if (op >= res + one) {
			op -= res + one;
			res += one << 1; /* <-- faster than 2 * one */
		}
		res >>= 1;
		one >>= 2;
	}

	/* Do arithmetic rounding to nearest integer */
	if (op > res) {
		res++;
	}

	return res;
}

/**
 * This is hard set of the motion state
 */
void motion_set_state(uint8_t mode, int8_t speed, uint8_t phase, uint8_t extra,
		uint8_t crc) {
	state.mode = mode;
	state.speed = speed;
	state.phase = phase;
	state.extra = extra;
	state.crc = crc;
	motion_write_state_to_vregs(state);
}

/**
 * Clear the current motion command, and stop
 */
int32_t motion_stop(void) {
	state.mode = 0;
	state.speed = 0;
	state.phase = 0;
	state.extra = 0;
	state.crc = 0;
	motion_write_state_to_vregs(state);

	return 0;
}

/* Return the Calibrate flag to show the encoder can be calibrated with the hall-sensors. */
uint8_t get_calibrate(void) {
	return calibrate;
}

/* Set calibrate flag to 0 or 1 to be able to calibrate the encoder with the hall-sensors. */
void set_calibrate(uint8_t value) {
	calibrate = value;
	return;
}

/*
 * This is initializer of the motion data
 * This function should only be called when the adc
 * is correctly initialized
 */
void motion_init(void) {
	motion_stop();
	touch_down_position = (!(address_get_side()) * TOUCH_DOWN_POSITION_L)
			+ (address_get_side() * TOUCH_DOWN_POSITION_R);
	stand_up_position = (!(address_get_side()) * STAND_UP_POSITION_L)
			+ (address_get_side() * STAND_UP_POSITION_R);
	lift_off_position = (!(address_get_side()) * LIFT_OFF_POSITION_L)
			+ (address_get_side() * LIFT_OFF_POSITION_R);

#ifdef DEBUG_VREGS
	vregs_write(VREGS_STAND_UP_POSITION_A, (uint8_t) (stand_up_position));
	vregs_write(VREGS_STAND_UP_POSITION_B, (uint8_t) (stand_up_position >> 8));
#endif
	return;
}

/* ------- OLD CODE ---------*/

//#include "position.h"
//#include "sequencer.h"
//#include "walk.h"
//#include "step.h"
//static int32_t time; /* The time what the function is called, kept constant during the function call*/
//static int8_t angle_error; /*The error that that should be controlled*/
//static int32_t new_dutycycle;
//static int32_t side_of_zebro;
//static int32_t angular_velocity = 0;
//static struct motion_timestamped_angle last_known_angle = { 0, 0 };
//int32_t motion_update_data(void) {
////TODO we should only do this in certain modes
//
//	uint8_t temp_angle;
//	uint8_t diff_angle;
//	int32_t temp_time;
//	int32_t diff_time;
//
//	temp_angle = position_get_current_index() * MOTION_SEGMENTS_PER_INDEX;
//	temp_time = time_get_time_ms();
//	if (temp_angle != last_known_angle.angle) {
//
//		diff_angle = temp_angle - last_known_angle.angle;
//		if (temp_angle < last_known_angle.angle) {
//			diff_angle += MOTION_SEGMENTS_PER_FULL_CIRCLE;
//		}
//		diff_time = temp_time - last_known_angle.timestamp;
//		if (temp_time < last_known_angle.timestamp) {
//			diff_time += TIME_MAX_TIME_MS;
//			/*
//			 * Time wrap-around
//			 * The virtual fase calculation still needs to be correct
//			 * Therefore the phase state should be updated accordingly state.
//			 */
//			phase = motion_virtual_angle(state.mode, TIME_MAX_TIME_MS);
//			motion_write_state_to_vregs(state);
//		}
//
//		angular_velocity = (diff_angle * MOTION_MILLISECOND_PER_SECOND)
//				/ diff_time;
//
//		/*
//		 * Update the data last_known_angle.
//		 */
//		angle = temp_angle;
//		last_known_angle.timestamp = temp_time;
//
//		data_update_flag = MOTION_FLAG_SET;
//
//	}
//	return temp_time;
//}
/**
 * Look at the drive command, the position data, and the time.
 * Use this data to choose how to actuate the h_bridge.

 int32_t motion_drive_h_bridge_simple() {
 // todo: implement proper function here.

 if (state.mode == 0) {
 h_bridge_disable();
 return 0;
 }

 vregs_write(VREGS_DEBUG_FLAG_6, state.speed);

 int32_t dutycycle;

 dutycycle = (((int32_t) state.speed) * 100) / 255;
 vregs_write(VREGS_DEBUG_FLAG_5, (uint8_t) dutycycle);

 h_bridge_lock_anti_phase(dutycycle);

 return 0;
 }


 *
 * Keeps track of where the motor should be.
 * For now this makes the motor turn at a constant speed

 int32_t motion_virtual_angle(int32_t motion_mode, int32_t time) {
 int32_t virtual_angle;
 int32_t side;
 side = address_get_side();
 Check on what side of the Zebro the motor is.
 if (side == ADDRESS_RIGHT) {
 Implement kinmatic equation:
 * Thetha(t)=Omega*t+Thetha(0)
 virtual_angle = ((state.speed * MOTION_SEGMENTS_PER_SECOND_PER_RPM)
 * time / MOTION_MILLISECOND_PER_SECOND + state.phase)
 % MOTION_SEGMENTS_PER_FULL_CIRCLE;
 vregs_write(VREGS_MOTION_VIRTUAL_ANGLE, virtual_angle);
 return (virtual_angle);
 } else {
 Implement kinmatic equation but motion is in reversed direction
 * Thetha(t)=Omega*t+Thetha(0)
 virtual_angle = ((state.speed * -1 * MOTION_SEGMENTS_PER_SECOND_PER_RPM)
 * time / MOTION_MILLISECOND_PER_SECOND
 + (MOTION_SEGMENTS_PER_FULL_CIRCLE - state.phase))
 % MOTION_SEGMENTS_PER_FULL_CIRCLE;
 return (virtual_angle);
 }
 }

 *
 * This function estimates where the leg is now
 * By again calculation the kinematic equations

 int32_t motion_estimated_currect_angle(int32_t time) {
 int32_t diff_time;
 diff_time = time - last_known_angle.timestamp;
 Temporal wrap-around
 if (time < last_known_angle.timestamp) {
 diff_time += TIME_MAX_TIME_MS;
 }
 //return (last_known_angle.angle+((diff_time*angular_velocity)/MOTION_SECOND_PER_MILLISECOND))%MOTION_FULL_CIRCLE;
 return (last_known_angle.angle);
 }
 *
 * Determine the error from the angle where we want to be.
 * Positive angle implies the motor should run slower
 * Negative angle implies the angle should run faster
 * The leg is circular therefore:
 *  both positive and negative angles exist, the smallest is chosen
 *  the function has to deal with wrap-around

 int32_t motion_angle_error(int32_t time) {
 int32_t virtual_angle, estimated_angle;
 int32_t angle_error, angle_error_positive, angle_error_negative;

 virtual_angle = motion_virtual_angle(state.mode, time);
 estimated_angle = motion_estimated_currect_angle(time);

 if (virtual_angle == estimated_angle) {
 angle_error = 0;
 } else if (virtual_angle < estimated_angle) {
 angle_error_positive = estimated_angle - virtual_angle;
 angle_error_negative = angle_error_positive
 - MOTION_SEGMENTS_PER_FULL_CIRCLE;
 if (angle_error_positive < MOTION_SEGMENTS_PER_HALF_CIRCLE) {
 angle_error = angle_error_positive;
 } else {
 angle_error = angle_error_negative;
 }
 } else { virtual_angle>estimated_angle
 angle_error_negative = estimated_angle - virtual_angle;
 angle_error_positive = angle_error_negative
 + MOTION_SEGMENTS_PER_FULL_CIRCLE;
 if (angle_error_positive < MOTION_SEGMENTS_PER_HALF_CIRCLE) {
 angle_error = angle_error_positive;
 } else {
 angle_error = angle_error_negative;
 }
 }
 return angle_error;
 }

 *
 * Go to the hall sensor that is closest to the given angle.
 * Uses round down of the angle to find the hall sensor.
 * Just rotates until the hall sensor is passed, then abruptly stops.

 int32_t motion_go_to_position_dumb(void) {
 int32_t position_index;

 position_index = state.phase / 10;
 if (position_index >= POSITION_NUM_OF_POSITIONS)
 return -1;
 if (position_index < 0)
 return -1;

 vregs_write(VREGS_DEBUG_FLAG_1, position_index);

 if (position_get_current_index() == position_index) {
 h_bridge_disable();
 }

 else {
 int32_t dutycycle;

 dutycycle = (((int32_t) state.speed) * 100) / 255;

 h_bridge_lock_anti_phase(dutycycle);
 }

 return 0;
 }

 void motion_turn(void) {
 angle_error = motion_angle_error(time);
 vregs_write(VREGS_MOTION_ANGLE_ERROR, angle_error);
 If the the motor is within the controllable limit use a P-controller to control it
 if (angle_error > -1 * MOTION_CONTROLLABLE_LIMIT
 && angle_error < MOTION_CONTROLLABLE_LIMIT) {
 The motor is only controlled when a new reliable data point is known
 if (data_update_flag == MOTION_FLAG_SET) {
 This is the implementation of the controller
 * For now this is a P controller
 new_dutycycle = MOTION_NEUTRAL_DUTYCYCLE
 - (MOTION_CONTROLLER_P * angle_error >> 2);

 Motor is not allowed to turn in the wrong direction
 if (((side_of_zebro == ADDRESS_RIGHT) && (state.speed > 0)
 && (new_dutycycle < MOTION_NEUTRAL_DUTYCYCLE))
 || ((side_of_zebro == ADDRESS_RIGHT) && (state.speed < 0)
 && (new_dutycycle > MOTION_NEUTRAL_DUTYCYCLE))
 || ((side_of_zebro == ADDRESS_LEFT) && (state.speed < 0)
 && (new_dutycycle < MOTION_NEUTRAL_DUTYCYCLE))
 || ((side_of_zebro == ADDRESS_LEFT) && (state.speed > 0)
 && (new_dutycycle > MOTION_NEUTRAL_DUTYCYCLE))) {
 new_dutycycle = MOTION_NEUTRAL_DUTYCYCLE;

 }
 Dutycycle has limits
 if (new_dutycycle < 2) {
 new_dutycycle = 2;
 }

 else if (new_dutycycle > 98) {
 new_dutycycle = 98;
 }
 For these dutycycles the motor has to little torque to move
 * therefore
 else if (new_dutycycle > 47 && new_dutycycle < 53) {
 new_dutycycle = 50;
 }

 Update dutycycle and actuate the motor
 dutycycle = new_dutycycle;
 h_bridge_lock_anti_phase(dutycycle);

 When the motor is still waiting to get started in the right direction
 * the flag should not be cleared
 if ((state.speed == 0)
 || (new_dutycycle != MOTION_NEUTRAL_DUTYCYCLE)) {
 data_update_flag = MOTION_FLAG_CLEAR;
 }

 }
 }
 If the motor is outside the controllable limit it idles until it is
 else {
 h_bridge_lock_anti_phase(MOTION_NEUTRAL_DUTYCYCLE);
 dutycycle = MOTION_NEUTRAL_DUTYCYCLE;
 data_update_flag = MOTION_FLAG_SET;
 }
 }*/
