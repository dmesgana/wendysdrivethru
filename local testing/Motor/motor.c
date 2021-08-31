/*
 * motor.c
 *
 *  Created on: Nov 10, 2020
 *      Author: md5jd
 */

#include "motor.h"
//#include <stdio.h>
//#include "rom_map.h"
#include "hw_memmap.h"
#include "pinmux.h"

void move(int num_steps)
{
    int direction = 0; int iter = 0;
    int steps_left = abs(num_steps); //check how to do absolute
    if(num_steps > 0)
    {
        direction = 1;
        iter = 0;
    }
    if(num_steps < 0)
    {
        direction = -1;
        iter = steps_left;
    }

    while(steps_left > 0){
        if(direction == 1){iter++;}
        if(direction == -1){iter--;}
        switch(iter%4){
        case 0:
            MAP_GPIOPinWrite(GPIOA0_BASE,0x00000001,0x00000001); //P45
            MAP_GPIOPinWrite(GPIOA2_BASE,0x00000040,0); //P21
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000001,0x00000001); //P55
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000080,0); //P15
        case 1:
            MAP_GPIOPinWrite(GPIOA0_BASE,0x00000001,0); //P45
            MAP_GPIOPinWrite(GPIOA2_BASE,0x00000040,0x00000040); //P21
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000001,0x00000001); //P55
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000080,0); //P15
        case 2:
            MAP_GPIOPinWrite(GPIOA0_BASE,0x00000001,0); //P45
            MAP_GPIOPinWrite(GPIOA2_BASE,0x00000040,0x00000040); //P21
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000001,0); //P55
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000080,0x00000080); //P15
        case 3:
            MAP_GPIOPinWrite(GPIOA0_BASE,0x00000001,0x00000001); //P45
            MAP_GPIOPinWrite(GPIOA2_BASE,0x00000040,0); //P21
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000001,0); //P55
            MAP_GPIOPinWrite(GPIOA3_BASE,0x00000080,0x00000080); //P15
        }
        steps_left--;
        MAP_UtilsDelay(8000000);
    }
}
