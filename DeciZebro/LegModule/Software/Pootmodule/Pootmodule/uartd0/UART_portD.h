/*
 * UART_portD.h
 *
 * Created: 07/12/2016 13:30:38
 *  Author: Cire
 */ 


#ifndef UART_PORTD_H_
#define UART_PORTD_H_

void uart_init(void); // initialization, baudrate is set as 115200

void UART_receive_complete (void);
bool UART_sleep_mode (void);

uint8_t UART_Receive( void );
void UART_Transmit( uint8_t data );
bool UART_DataReady( void );

bool UART_transmit_enable (void);
bool UART_transmit_disable (void);

uint8_t UART_Send_FlashStr( const char * str );
uint8_t UART_Send_RAMStr( char * str );

bool UART_Receive_timeout(void);
void UART_Receive_timeout_clear(void);


#define UART_NEWLINE {UART_Transmit(0x0d); UART_Transmit(0x0a);}




#endif /* UART_PORTD_H_ */