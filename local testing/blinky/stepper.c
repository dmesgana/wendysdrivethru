/*
 * stepper.c
 *
 *  Created on: Dec 8, 2020
 *      Author: md5jd
 */
#include "hw_types.h"
#include "hw_memmap.h"
#include "rom_map.h"
#include "uart.h"
#include "gpio.h"
#include "utils.h"

#include "pinmux.h"
#include "stdio.h"
#include "encoder.h"

void move(int num_steps, int rpm)
{
    if(num_steps == 0){
        printf("can't move by nothing");
        return;
    }
    int direction = 0; int iter = 0;
    int steps_left = abs(num_steps);

    //determines the direction of the motor
    //positive = clockwise
    //negative = counter-clockwise
    if(num_steps > 0)
    {
        direction = 1; iter = 0;
    }

    if(num_steps < 0)
    {
        direction = -1; iter = steps_left;
    }

    //runs the while loop until there are no more steps
    while(steps_left > 0){
        //either increments or decrements the iter
        //iter determines the direction of the switch cases
        if(direction == 1){iter++;}
        if(direction == -1){iter--;}

        //switch cases for the different states of the unipolar motor
        switch(iter % 4){
        case 0:
            MAP_GPIOPinWrite(GPIOA3_BASE,0x80,0x80); //P45
            MAP_GPIOPinWrite(GPIOA3_BASE,0x2,0); //P21
            MAP_GPIOPinWrite(GPIOA0_BASE,0x40,0x40); //P62
            MAP_GPIOPinWrite(GPIOA2_BASE,0x40,0); //P15
            break;
        case 1:
            MAP_GPIOPinWrite(GPIOA3_BASE,0x80,0); //P45
            MAP_GPIOPinWrite(GPIOA3_BASE,0x2,0x2); //P21
            MAP_GPIOPinWrite(GPIOA0_BASE,0x40,0x40); //P62
            MAP_GPIOPinWrite(GPIOA2_BASE,0x40,0); //P15
            break;
        case 2:
            MAP_GPIOPinWrite(GPIOA3_BASE,0x80,0); //P45
            MAP_GPIOPinWrite(GPIOA3_BASE,0x2,0x2); //P21
            MAP_GPIOPinWrite(GPIOA0_BASE,0x40,0); //P62
            MAP_GPIOPinWrite(GPIOA2_BASE,0x40,0x40); //P15
            break;
        case 3:
            MAP_GPIOPinWrite(GPIOA3_BASE,0x80,0x80); //P45
            MAP_GPIOPinWrite(GPIOA3_BASE,0x2,0); //P21
            MAP_GPIOPinWrite(GPIOA0_BASE,0x40,0); //P62
            MAP_GPIOPinWrite(GPIOA2_BASE,0x40,0x40); //P15
            break;
        }
        //decrement steps
        steps_left--;

        //determines the speed of the motor
        //the less in delay the faster the motor
        MAP_UtilsDelay(rpm); //presets -> fast=33333, mid=66666, slow=133332
    }
}

int EncToStep(int encPosition)
{ //full turn for encoder = 16384
    return (encPosition/16384)*200;
}


