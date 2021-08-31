/*
 * Stepper.h
 *
 *  Created on: Dec 8, 2020
 *      Author: md5jd
 */

#ifndef STEPPER_H_
#define STEPPER_H_

void move(int num_steps, int rpm);

int EncToStep(int encPosition);

#endif /* STEPPER_H_ */
