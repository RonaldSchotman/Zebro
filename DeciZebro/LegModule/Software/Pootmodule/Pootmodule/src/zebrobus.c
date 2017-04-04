/**
 * POOT/ DECI ZEBRO LEG MODULE
 * The Zebro Project
 * Delft University of Technology
 * 2016/2017
 *
 * Filename: zebrobus.c
 *
 * Description:
 * Code for the interface with the ZebroBus
 * The ZebroBus uses the TWIE bus
 *
 * authors
 * Piet De Vaere -- Piet@DeVae.re
 * Daniel Booms -- d.booms@solcon.nl
 */

#include <stdint.h>
#include <avr/io.h>

#include "../inc/zebrobus.h"
#include "../inc/vregs.h"
#include "../inc/address.h"
#include "../inc/interrupts.h"
#include "../inc/errors.h"
#include "../inc/time.h"
#include "../inc/motion.h"

static int8_t zebrobus_is_master = 0;
static int8_t state = ZEBROBUS_STATE_IDLE;
static uint8_t request_address_base = 0x00;
static uint8_t request_address = 0x00;

static struct zebrobus_write_request write_queue[ZEBROBUS_SIZE_OF_QUEUE];
static int8_t queue_start = 0, queue_end = 0;

//TODO: implement ignoring of read requests to a multicast address
//TODO: implement serial nr. it can be stored in non volatile memory
//TODO: implement motor voltage field it can be stored in non volatile memory
//TODO: implement the quick_status field

/**
 * Put a write request in the queue, this function should only be called
 * by the interrupt routine, and is *not* reentrant.
 */
int8_t zebrobus_put_write_request(uint32_t address, uint8_t data){

	/* check if the queue is full */
	if (((queue_end + 1) % ZEBROBUS_SIZE_OF_QUEUE) == queue_start){
		return ZEBROBUS_QUEUE_FULL;
	}

	/* insert new item, and move the end of the queue */
	write_queue[queue_end].address = address;
	write_queue[queue_end].data = data;
	queue_end = (queue_end + 1) % ZEBROBUS_SIZE_OF_QUEUE;

	return 0;
}

/**
 * Get a write request from the queue, this function should only be called
 * by the task code, and is *not* reentrant.
 */
struct zebrobus_write_request zebrobus_get_write_request(void){
	struct zebrobus_write_request return_struct;

	interrupts_disable();

	/* if there is nothing in the queue, return */
	if (queue_start == queue_end){
		interrupts_enable();
		return (struct zebrobus_write_request) {UINT32_MAX, 0};
	}

	/* otherwise, return the oldest element in the queue, and move the start */
	/* first make a copy, then increment begin.
	 * because otherwise the interrupt might think the element was already
	 * removed from the queue, before we copied it.
	 */

	return_struct = write_queue[queue_start];
	queue_start = (queue_start + 1) % ZEBROBUS_SIZE_OF_QUEUE;
	interrupts_enable();

	return return_struct;


}

/**
 * Initialise the ZebroBus (TWIE) interface in slave mode.
 */
int8_t zebrobus_slave_init(void){
	//GPIO_InitTypeDef  GPIO_InitStruct;

	zebrobus_is_master = 0;

	/* enable clock to periferal */
	sysclk_enable_module(SYSCLK_PORT_E, SYSCLK_TWI);

	/* set up the pins */
	ZEBROBUS_PORT.DIRSET = ZEBROBUS_SDA_PIN | ZEBROBUS_SCL_PIN | ZEBROBUS_ENABLE_PIN;
	ZEBROBUS_PORT.ZEBROBUS_SDA_PINCTRL |= PORT_OPC_WIREDANDPULL_gc;
	ZEBROBUS_PORT.ZEBROBUS_SCL_PINCTRL |= PORT_OPC_WIREDANDPULL_gc;
	ZEBROBUS_PORT.OUTSET = ZEBROBUS_ENABLE_PIN;
	
	/* enable the ISR in the NVIC, give it a low priority */
	
	TWIE.SLAVE.CTRLB |= TWI_SLAVE_INTLVL_LO_gc;
	//NVIC_EnableIRQ(I2C1_IRQn);
	//NVIC_SetPriority(I2C1_IRQn, 3);

	/*set the slave address, enable general call address 0x00 */
	TWIE.SLAVE.ADDR = ZEBROBUS_GENERAL_CALL_ENABLE | (address_get_zebrobus_address() << 1);

	vregs_write(VREGS_ZEBROBUS_ADDRESS, address_get_zebrobus_address());

	/* generate interrupt on
	 * * Address match
	 * * Non empty receive buffer
	 * * Empty transmit buffer
	 * * Stop bit
	 * *
	 */
	TWIE.SLAVE.CTRLA |= TWI_SLAVE_DIEN_bm | TWI_SLAVE_APIEN_bm | TWI_SLAVE_PIEN_bm;
	
	/*Enable the TWI slave */
	TWIE.SLAVE.CTRLB |= TWI_SLAVE_ENABLE_bm;
	
	return 0;
}

/**
 * The interrupt handler for ZebroBus (I2C1)
 */
ISR(TWIE_TWIS_vect){
	uint8_t status_register;

	//todo: error checking

	/* get a copy of the status register */
	status_register = TWIE.SLAVE.STATUS;

	/* on stop condition, reset state machine */
	if((status_register & TWI_SLAVE_APIF_bm) && !(status_register & TWI_SLAVE_AP_bm)){
		request_address = request_address_base;
		/* Clear flag */
		TWIE.SLAVE.STATUS |= TWI_SLAVE_APIF_bm;
		/* Complete transaction */
		TWIE.SLAVE.CTRLB |= TWI_SLAVE_CMD_COMPTRANS_gc;
		state = ZEBROBUS_STATE_IDLE;
		return;
	}

	/* on address match */
	if((status_register & TWI_SLAVE_APIF_bm) && (status_register & TWI_SLAVE_AP_bm)){
		/* Clear flag */
		TWIE.SLAVE.STATUS |= TWI_SLAVE_APIF_bm;
		/* If we are about to receive some data, return.
		 * We will come back when the data has been transfered.
		 * On the other hand, if we have to transmit, we will have
		 * to prepare data to be transmitted.
		 */
		TWIE.SLAVE.CTRLB |= TWI_SLAVE_CMD_RESPONSE_gc;
	}

	/* if we are to transmit data */
	if(status_register & TWI_SLAVE_DIF_bm){
		/* transmit the byte, and increment the vreg address to read from */
		TWIE.SLAVE.DATA = vregs_read_buffer((uint8_t) request_address++);
		TWIE.SLAVE.CTRLB |= TWI_SLAVE_CMD_RESPONSE_gc;
		/* the vregs are circular */
		if(request_address) request_address %= VREGS_FILE_SIZE;
	}

	/* if we are to receive data */
	else{
		switch(state){
		/* the first byte we receive is the address of the read / write */
		case ZEBROBUS_STATE_IDLE:
			state = ZEBROBUS_STATE_RECEIVED_ADDR;
			request_address_base = TWIE.SLAVE.DATA;
			request_address = request_address_base;
			TWIE.SLAVE.CTRLB |= TWI_SLAVE_CMD_RESPONSE_gc;
			break;

		/* in case of a write, the second byte is the data to be written,
		 * when more bytes are written, they are written to the next position
		 * in the vregs */
		case ZEBROBUS_STATE_RECEIVED_ADDR:
			zebrobus_put_write_request(request_address++, TWIE.SLAVE.DATA);
			TWIE.SLAVE.CTRLB |= TWI_SLAVE_CMD_RESPONSE_gc;
			/* the vregs are circular */
			if(request_address) request_address %= VREGS_FILE_SIZE;
			break;
		}
	}
}

/**
 * Process the write requests from ZebroBus.
 * Should be called from task code, is not reentrant
 */
int32_t zebrobus_process_write_requests(void){
	int32_t safety_counter;
	for(safety_counter = 0; safety_counter < ZEBROBUS_SIZE_OF_QUEUE;
			safety_counter++){

		struct zebrobus_write_request request;
		request = zebrobus_get_write_request();
		/* break when the queue is empty */
    	if(request.address == UINT32_MAX) break;

		/* process the write request */

    	switch(request.address){
    	case VREGS_MOTION_MODE:
    	case VREGS_MOTION_SPEED:
    	case VREGS_MOTION_PHASE:
    	case VREGS_MOTION_EXTRA:
    	case VREGS_MOTION_CRC:
    	case VREGS_MOTION_UPDATE:
    		motion_new_zebrobus_data(request.address, request.data);
    		break;

    	case VREGS_TEST_FIELD:
        	vregs_write(request.address, request.data);
        	break;

    	case VREGS_SYNC_COUNTER:
    		time_set_time(request.data);
    		break;


    	case VREGS_SERIAL_ID:
    		// TODO: do this propery
    		vregs_write(VREGS_SERIAL_ID, request.data);
    		break;

    	case VREGS_ERROR_COUNTER:
    		errors_reset_errors(ERRORS_ERRORS_RESET_SAFETY);
    		break;

    	case VREGS_EMERGENCY_STOP:
    		errors_reset_emergency_stop(request.data);
    		break;

    	default:
    		break;

    	}
	}

	return safety_counter;
}

