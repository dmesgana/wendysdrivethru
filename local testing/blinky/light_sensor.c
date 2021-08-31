/*
 * light_sensor.c
 *
 *  Created on: Nov 17, 2020
 *      Author: Kwadwo
 */

#include "light_sensor.h"
#include "hw_memmap.h"
#include "rom_map.h"
#include "adc.h"

#define NO_OF_SAMPLES       128

unsigned long pulAdcSamples[4096];


float
getLightLevel(void)

{
    //
    // Initialize Array index for multiple execution
    //
    unsigned int  uiChannel;
    unsigned int  uiIndex=0;
    unsigned long ulSample;
    uiIndex=0;
    float adcVal = 0;
    float adcSum = 0;

    //
    // Read inputs from user
    //

    //
    // Pinmux for the selected ADC input pin

    //uiChannel = ADC_CH_0; // pin 57
    uiChannel = ADC_CH_1; // pin 58

    //
    // Configure ADC timer which is used to timestamp the ADC data samples
    //
    MAP_ADCTimerConfig(ADC_BASE,2^17);

    //
    // Enable ADC timer which is used to timestamp the ADC data samples
    //
    MAP_ADCTimerEnable(ADC_BASE);

    //
    // Enable ADC module
    //
    MAP_ADCEnable(ADC_BASE);

    //
    // Enable ADC channel
    //

    MAP_ADCChannelEnable(ADC_BASE, uiChannel);

    while(uiIndex < NO_OF_SAMPLES + 4)
    {
        if(MAP_ADCFIFOLvlGet(ADC_BASE, uiChannel))
        {
            ulSample = MAP_ADCFIFORead(ADC_BASE, uiChannel);
            pulAdcSamples[uiIndex++] = ulSample;
        }
    }

    MAP_ADCChannelDisable(ADC_BASE, uiChannel);

    uiIndex = 0;

    //
    // Print out ADC sample average
    //

    while(uiIndex < NO_OF_SAMPLES)
    {
        adcSum += (pulAdcSamples[4+uiIndex] >> 2 ) & 0x0FFF;
        uiIndex++;
    }

    adcVal =  adcSum/NO_OF_SAMPLES;

    return adcVal;
}


