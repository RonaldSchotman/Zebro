/*
 * I2c.c
 *
 * Created: 8-5-2014 13:38:14
 *  Author: Martijn
 */ 
/*
Voor gebruik van deze code met de Ultrasoon sensor
Vergeet niet de levelshifter toe te passen.
En deze code doet het mischien niet ook al is hij wle te bouwen.
Graag iemand die hem uittest.
*/
#define  F_CPU 2000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <util/twi.h>

#define ENABLE_UART_E0	1
#define E0_BAUD			115800
#define E0_CLK2X		0
#include "uart.h"

int static Ultrasoon = 0; //integer voor Ultrasoon;

#include "avr_compiler.h"      // deze 3 bestanden zijn nodig voor het gebruik van I2C
#include "twi_master_driver.h"
#include "twi_slave_driver.h"

/*! Defining an example slave address. */
#define SLAVE_ADDRESS    0x55

/*! Defining number of bytes in buffer. */
#define NUM_BYTES        8

/*! CPU speed 2MHz, BAUDRATE 100kHz and Baudrate Register Settings */
#define CPU_SPEED   2000000
#define BAUDRATE	100000
#define TWI_BAUDSETTING TWI_BAUD(CPU_SPEED, BAUDRATE)


/* Global variables */
TWI_Master_t twiMaster;    /*!< TWI master module. */
TWI_Slave_t twiSlave;      /*!< TWI slave module. */

/*! Buffer with test data to send.*/ // Dit is voor mogelijk testen het is niet nodig en weet niet wat voor invloed hij heeft.
uint8_t sendBuffer[NUM_BYTES] = {0x55, 0xAA, 0xF0, 0x0F, 0xB0, 0x0B, 0xDE, 0xAD};

/*! Simple function that invert the received value in the sendbuffer. This
 *  function is used in the driver and passed on as a pointer to the driver.
 */
void TWIC_SlaveProcessData(void)
{
	uint8_t bufIndex = twiSlave.bytesReceived;
	twiSlave.sendData[bufIndex] = (~twiSlave.receivedData[bufIndex]);
}

void TheWait(void)
{
	uart_putc(&uartE0, Ultrasoon);
	_delay_ms(500);
}

/*! /brief Example current code
 *
 *  Example code that reads the key pressed and show a value from the buffer,
 *  sends the value to the slave and read back the processed value which will
 *  be inverted and displayed after key release.
 */

/*! /Brief Example new code
 *  
 *  That reads the data which the Ultrasoon sensor gives.
 *  Sends the data to putty so the user can see it.
 *  repeats the same every 500 ms. not sooner and not later
 *  
 */

int main(void)
{
	
	/*Uart */
	init_uart(&uartE0, &USARTE0, F_CPU, E0_BAUD, E0_CLK2X);		//initialiseer uart
	PMIC.CTRL = PMIC_LOLVLEN_bm;
	sei();
	/*I2C  */
	PORTC.DIRSET = PIN1_bm|PIN0_bm; // SDA 0 SCL 1
	PORTC.PIN0CTRL = PORT_OPC_WIREDANDPULL_gc; // Pullup SDA
	PORTC.PIN1CTRL = PORT_OPC_WIREDANDPULL_gc; // Pullup SCL

/*	
	// Initialize PORTE for output and PORTD for inverted input. 
	//PORTE.DIRSET = 0xFF;
	//PORTD.DIRCLR = 0xFF;
	PORTCFG.MPCMASK = 0xFF;
	//PORTD.PIN0CTRL |= PORT_INVEN_bm;
//      PORTCFG.MPCMASK = 0xFF;
//      PORTD.PIN0CTRL = (PORTD.PIN0CTRL & ~PORT_OPC_gm) | PORT_OPC_PULLUP_gc;
	
//  Enable internal pull-up on PC0, PC1.. Uncomment if you don't have external pullups
//	PORTCFG.MPCMASK = 0x03; // Configure several PINxCTRL registers at the same time
//	PORTC.PIN0CTRL = (PORTC.PIN0CTRL & ~PORT_OPC_gm) | PORT_OPC_PULLUP_gc; //Enable pull-up to get a defined level on the switches
*/
	

	/* Initialize TWI master. */
	TWI_MasterInit(&twiMaster,
	               &TWIC,
	               TWI_MASTER_INTLVL_LO_gc,
	               TWI_BAUDSETTING);

	/* Initialize TWI slave. */
	TWI_SlaveInitializeDriver(&twiSlave, &TWIC, TWIC_SlaveProcessData);
	TWI_SlaveInitializeModule(&twiSlave,
	                          SLAVE_ADDRESS,
	                          TWI_SLAVE_INTLVL_LO_gc);

	/* Enable LO interrupt level. */
	PMIC.CTRL |= PMIC_LOLVLEN_bm;
	sei();

	//uint8_t BufPos = 0;
	
	while (1) {
 // Dit is voor test code en is niet nodig mag weg als alles het doet
 /*
       while(!PORTD.IN);  Wait for user to press button       
          
		switch(PORTD.IN){
			case (PIN0_bm):  BufPos = 0; break;
			case (PIN1_bm):  BufPos = 1; break;
			case (PIN2_bm):  BufPos = 2; break;
			case (PIN3_bm):  BufPos = 3; break;
			case (PIN4_bm):  BufPos = 4; break;
			case (PIN5_bm):  BufPos = 5; break;
			case (PIN6_bm):  BufPos = 6; break;
			case (PIN7_bm):  BufPos = 7; break;
			default:    break;
		}
*/
  // Dit is voor test code en is niet nodig mag weg als alles het doet
/*
		// Show the byte to send while holding down the key. 
		while(PORTD.IN != 0x00){
			PORTE.OUT = sendBuffer[BufPos];
		}
*/
		TheWait();
		TWI_MasterWriteRead(&twiMaster,
		                    SLAVE_ADDRESS,
		                    &sendBuffer[Ultrasoon], //moet een pointer zijn, nu alleen nog de juiste
		                    1,					// wat betekenen deze twee 1'en ?
		                    1);


		while (twiMaster.status != TWIM_STATUS_READY) {
			/* Wait until transaction is complete. */
		}
 // Dit is voor test code en is niet nodig mag weg als alles het doet		
/*
		// Show the sent byte received and processed on LEDs. 
		PORTE.OUT = (twiMaster.readData[0]);
                
                while(PORTD.IN); // Wait for user to release button 
*/				
	}
}

/*! TWIC Master Interrupt vector. */
ISR(TWIC_TWIM_vect)
{
	TWI_MasterInterruptHandler(&twiMaster);
}

/*! TWIC Slave Interrupt vector. */
ISR(TWIC_TWIS_vect)
{
	TWI_SlaveInterruptHandler(&twiSlave);
}
