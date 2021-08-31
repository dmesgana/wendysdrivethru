/*
 * encoder.c
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
#include "prcm.h"

#include "pinmux.h"
#include "encoder.h"

void RS485Transmit(unsigned char data){
    MAP_GPIOPinWrite(GPIOA0_BASE, 0x80, 0x80); //Pin 62
    MAP_UARTCharPut(UARTA0_BASE, data);
    MAP_UtilsDelay(50000);
    return;
}

void RS485Receive(){
    MAP_GPIOPinWrite(GPIOA0_BASE, 0x80, 0); //Pin 62
    MAP_UtilsDelay(50000);
    return;
}

//cmds -> 0x54 (values within 1 turn), 0x55 (# of turns)
unsigned int EncPosition(){
    char enc_read[3]; //0->'cmd, 1->low, 2->high
    char enc_cmd;
    unsigned int enc_low;
    unsigned int enc_high;

    int i = 0;
    while(MAP_UARTCharsAvail(UARTA0_BASE)){
        /*if(i == 3){
            printf("CharsAvail exceeded 3 characters\n");
            break;
        }*/
        enc_read[i] = MAP_UARTCharGetNonBlocking(UARTA0_BASE);
        /*if(MAP_UARTCharGetNonBlocking(UARTA0_BASE) == -1){
            printf("*ERROR* No characters in receive FIFO\n");
        }*/
        i++;
    }
    enc_cmd = enc_read[0];
    enc_low = (unsigned int) enc_read[1];
    //remove checksum bits and shift to upper byte
    enc_high = ((unsigned int)(enc_read[2] & CHECKSUM_MASK)) << 8;

    //printf("cmd:\t0x%x\n", enc_cmd);
    //printf("low:\t0x%x\n", enc_low);
    //printf("high:\t0x%x\n", enc_high);

    return enc_high | enc_low;
}

void SetupEnc(){
    MAP_UARTConfigSetExpClk(UARTA0_BASE, MAP_PRCMPeripheralClockGet(PRCM_UARTA0), 2000000, (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));
    return;
}
