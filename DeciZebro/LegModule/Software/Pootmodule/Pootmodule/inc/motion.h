/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: motion.h
 *
 * Description:
 * Translates zebrobus commands into action on the zebrobus
 *
 * Authors:
 * Daniël Booms -- d.booms@solcon.nl
 */


#ifndef __MOTION_H_
#define __MOTION_H_

struct motion_state{
	uint8_t mode;
	uint8_t speed; /*speed*10=RPM*/
	uint8_t phase; /*between 0 and 239, steps of 1.5 degree. 1/240 piece of a circular arc is the basic unit*/
	uint8_t extra;
	uint8_t crc;
};

struct motion_timestamped_angle{
	int32_t angle;
	int32_t timestamp;
};

#define MOTION_MODE_STOP		0
#define MOTION_MODE_STAND_UP	1
#define MOTION_MODE_WALK		2

#define MOTION_WALK_STATE_UNKNOWN			0
#define MOTION_WALK_STATE_READY_TO_WALK		1
#define MOTION_WALK_STATE_WALK				2
#define MOTION_WALK_STATE_READY_TO_ROTATE	3
#define MOTION_WALK_STATE_ROTATE			4


int8_t motion_new_zebrobus_data(uint32_t address, uint8_t data);
void motion_set_state(uint8_t mode, int8_t speed, uint8_t phase,
uint8_t extra, uint8_t crc);
int8_t motion_validate_state(struct motion_state motion_state);
int8_t motion_write_state_to_vregs(struct motion_state motion_state);
int8_t motion_drive_h_bridge(void);
int8_t motion_stop(void);
void motion_init(void);

#endif /* __MOTION_H_ */