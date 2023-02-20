#include <Servo.h>
#include <Romi32U4.h>
#include <PololuRPiSlave.h>


typedef enum STATE_TYPE
{
  READ,
  MOVE,
  HEADLESS
}STATE_TYPE;

STATE_TYPE state = READ;

void setup() {
  // put your setup code here, to run once:

  //Set up I2C stuff?

}

void loop() {
  // put your main code here, to run repeatedly:
    switch(state)
  {
    case READ:
      //read info from I2C buffer

      //store data in array

      //check the state byte

      //if state bit is 0 go to run

      //if state byte is 1 go to follow

      //if neither then go to headless
    break;      

    case MOVE:
      //check the turn and move bytes

      //if move byte and turn byte == 0 then return to read

      //if move byte == 1 then calculate forward movement
        
      
      //check if turn bit is high or not
        //add the base speed with the left and right speeds
      
      //set the motor speeds

      //go to the read state
    break;
 
    case HEADLESS:
      //turn in random direction (generate random number between 0 and 300 for each motor)

      //turn for a random amount of time (maybe pick random encoder number?)

      //move forward at middle speed (150) for both motors

      //move for a second or two

      //go back to read state
    break;    
  } 
}

//TODO: change this to return a value later
//the difference between run and follow is the direction of the motors
uint16_t move_calc(uint16_t error, uint8_t run)
{
  //check the run bit and determine what to do with the error

  //run proportional controller with error passed in

  //caluclate base speed from controller

  //return value calculated
}


//speeds is an array passed in by reference so it can be modifed
void turn_calc(uint16_t error, uint16_t turn, uint16_t &speeds)
{
  //run proportional controller with error passed in

  //check turn bit to determine which motor to apply speeds to

  //update speed in array passed in
}


