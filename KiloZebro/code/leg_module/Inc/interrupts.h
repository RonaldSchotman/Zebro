/**
 * POOT
 * The Zebro Project
 * Delft University of Technology
 * 2016
 *
 * Filename: interupts.h
 *
 * Description:
 * Header file for interupts.c
 * This file helps with enabling and disabling interrupts
 *
 * Authors:
 * Piet De Vaere -- Piet@DeVae.re
 */

#ifndef __INTERUPTS_H__
#define __INTERUPTS_H__

#include "stdint.h"

int32_t interrupts_enable();
int32_t interrupts_disable();


#endif /* __INTERUPTS_H__ */
