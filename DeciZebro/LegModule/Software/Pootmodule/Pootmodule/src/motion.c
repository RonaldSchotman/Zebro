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
 */

// Todo: implement signed speed field. Or maby we shouldn't.

#include <stdint.h>
#include <avr/io.h>
#include "../inc/motion.h"
#include "../inc/vregs.h"
#include "../inc/hbridge.h"
#include "../inc/address.h"
#include "../inc/time.h"
#include "../inc/encoder.h"


static struct motion_state state = {0,0,0,0,0};
static struct motion_state new_state = {0,0,0,0,0};
static struct motion_timestamped_angle last_known_angle = {0,0};
//static int32_t dutycycle = MOTION_NEUTRAL_DUTYCYCLE;
//static int32_t angular_velocity = 0;
static int8_t data_update_flag = 1;
static uint32_t timestamp; /* The time what the function is called, kept constant during the function call*/
//static int8_t angle_error; /*The error that that should be controlled*/
//static int32_t new_dutycycle;
static int8_t side_of_zebro;
static uint8_t walk_state = 0;
static uint8_t next_walk_state = 0;
static uint8_t parity = 0;

/**
 * Process data send to any of the addresses in the motion control range.
 */
int8_t motion_new_zebrobus_data(uint32_t address, uint8_t data){

    switch (address){

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
		if(!motion_validate_state(new_state)){
			state = new_state;
			motion_write_state_to_vregs(state);
			data_update_flag = 1;
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
int8_t motion_write_state_to_vregs(struct motion_state motion_state){
	vregs_write(VREGS_MOTION_MODE, motion_state.mode);
	vregs_write(VREGS_MOTION_SPEED, (uint8_t)(motion_state.speed));
	vregs_write(VREGS_MOTION_PHASE, motion_state.phase);
	vregs_write(VREGS_MOTION_EXTRA, motion_state.extra);
	vregs_write(VREGS_MOTION_CRC, motion_state.crc);

	return 0;
}


/**
 * Stub for the state validator.
 * return zero is state is OK.
 */
int8_t motion_validate_state(struct motion_state motion_state){
	return 0;
}


/**
 * Look at the drive command, the position data, and the time.
 * Use this data to choose how to actuate the h_bridge.
 */
int8_t motion_drive_h_bridge(void){
	timestamp = time_get_time_ms();
	switch (state.mode){
	case MOTION_MODE_STOP:
		hbridge_disable();
	case MOTION_MODE_STAND_UP:
		if(encoder_get_hall_state()){
			hbridge_sign_magnitude(side_of_zebro, (1<<15));
			walk_state = MOTION_WALK_STATE_UNKNOWN;
		}
		else{
			hbridge_disable();
			walk_state = MOTION_WALK_STATE_READY_TO_WALK;
		}
	case MOTION_MODE_WALK:
		
		switch(walk_state){
		case MOTION_WALK_STATE_UNKNOWN:
			hbridge_disable();
			next_walk_state = MOTION_WALK_STATE_UNKNOWN;
		case MOTION_WALK_STATE_READY_TO_WALK:
			if (parity){
				if (timestamp < 500){
					hbridge_sign_magnitude(side_of_zebro, (1<<15));
					next_walk_state = MOTION_WALK_STATE_WALK;
				}
				else{
					next_walk_state = MOTION_WALK_STATE_READY_TO_WALK;
				}
			}
			else{
				if (timestamp > 500){
					hbridge_sign_magnitude(side_of_zebro, (1<<15));
					next_walk_state = MOTION_WALK_STATE_WALK;
				}
				else{
					next_walk_state = MOTION_WALK_STATE_READY_TO_WALK;
				}
			}
		case MOTION_WALK_STATE_WALK:
			if (encoder_get_hall_state()){
				hbridge_disable();
				next_walk_state = MOTION_WALK_STATE_READY_TO_ROTATE;
			}
			else {
				next_walk_state = MOTION_WALK_STATE_WALK;
			}
		case MOTION_WALK_STATE_READY_TO_ROTATE:
		if (parity){
			if (timestamp > 500){
				hbridge_sign_magnitude(side_of_zebro, (1<<15));
				next_walk_state = MOTION_WALK_STATE_ROTATE;
			}
			else{
				next_walk_state = MOTION_WALK_STATE_READY_TO_ROTATE;
			}
		}
		else{
			if (timestamp < 500){
				hbridge_sign_magnitude(side_of_zebro, (1<<15));
				next_walk_state = MOTION_WALK_STATE_ROTATE;
			}
			else{
				next_walk_state = MOTION_WALK_STATE_READY_TO_ROTATE;
			}
		}
		case MOTION_WALK_STATE_ROTATE:
		if (encoder_get_hall_state()){
			next_walk_state = MOTION_WALK_STATE_ROTATE;
		}
		else {
			hbridge_disable();
			next_walk_state = MOTION_WALK_STATE_READY_TO_WALK;
		}
							 	
		}
		walk_state = next_walk_state;
		
	}
	
	return 0;
}

/**
 * This is hard set of the motion state
 */
void motion_set_state(uint8_t mode, int8_t speed, uint8_t phase,
		uint8_t extra, uint8_t crc){
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
int8_t motion_stop(void){
	state.mode = 0;
	state.speed = 0;
	state.phase = 0;
	state.extra = 0;
	state.crc = 0;
	motion_write_state_to_vregs(state);

	return 0;
}

/**
 * This is initialiser of the motion data
 * This function should only be called when the position
 * and the time are correctly initialised
 * position and time data is needed.
 */
void motion_init(void){
    uint8_t address = address_get_position();
	if ((address == 0) || (address == 2) || (address == 7)){
		parity = 0;
	}
	else{
		parity = 1;
	}
	
	last_known_angle.timestamp = time_get_time_ms();
	side_of_zebro = address_get_side();
	
   // last_known_angle.angle = position_get_current_index()*MOTION_SEGMENTS_PER_INDEX;
}



