/**
 * Leg Module Deci Zebro
 * The Zebro Project
 * Delft University of Technology
 * 2017
 *
 * Filename: interrupts.h
 *
 * Description:
 * This file helps with enabling and disabling interrupts
 * It keeps a counter of how many times interrupts have been
 * enabled and disabled, so that we do not accidentally enable
 * Interrupts when we should not. For example in nested functions.
 *
 * Authors:
 * Daniel Booms -- d.booms@solcon.nl
 * Piet De Vaere -- Piet@DeVae.re
 * 
 */


#ifndef INTERRUPTS_H_
#define INTERRUPTS_H_

#include "asf.h"

int8_t interrupts_enable(void);
int8_t interrupts_disable(void);

#endif /* INTERRUPTS_H_ */