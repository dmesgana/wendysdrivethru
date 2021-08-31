/*
 * encoder.h
 *
 *  Created on: Dec 8, 2020
 *      Author: md5jd
 */

#ifndef ENCODER_H_
#define ENCODER_H_

#define CHECKSUM_MASK 0x3F
// 0011 1111

void RS485Transmit(unsigned char data);
void RS485Receive();
unsigned int EncPosition();
void SetupEnc();


#endif /* ENCODER_H_ */
