#include <Servo.h>
#include <Romi32U4.h>
#include <PololuRPiSlave.h>
#include <Romi32U4Motors.h>


typedef enum STATE_TYPE
{
  READ,
  MOVE,
  HEADLESS
}STATE_TYPE;

STATE_TYPE state = READ;

// struct data
// {
//   bool turn, move, run, mode;  
//   uint16_t error;
// }

struct Data
{
  bool yellow, green, red;
  bool buttonA, buttonB, buttonC;

  int16_t leftMotor, rightMotor;
  uint16_t batteryMillivolts;
  uint16_t analog[6];

  bool playNotes;
  char notes[14];

  int16_t leftEncoder, rightEncoder;
};
/*Code for data struct is sourced and modifed from Pololu ROMIRPiSlaveDemo code*/
PololuRPiSlave<struct Data,5> MCU; //TODO: need to figure out how to change this to what I need


void setup() {

  //Set up MCU as I2C peripheral with address of 20
  MCU.init(20);

}

void loop() {
  uint16_t move_val = 0;
  uint16_t turn_val = 0;
  uint16_t turn_vals[2] = {0,0};
  long rand_left = 0;
  long rand_right = 0;
  switch(state)
  {
    case READ:
      //update buffer to get latest data
      //data sent from pi is stored in the data struct
      MCU.updateBuffer();

      //check the move bit to check which state to go to
      if(MCU.buffer.mode == 1)
      {
        state = MOVE;
      }
      else
      {
        state = HEADLESS;        
      }
    break;      

    case MOVE:
      //check the turn and move bytes
      //not moving or turning so just go back to read
      if((MCU.buffer.move == 0) && (MCU.buffer.turn == 0))      
      {
        state = READ;
      }
      
      //calculate the forward movment if the bit is high
      if(MCU.buffer.move == 1) 
      {
        move_val = move_calc(MCU.buffer.error, MCU.buffer.run);        
      }     
      
      //calculate the turn movement if the bit is high
      if(MCU.buffer.turn == 1)  
      {
        turn_calc(MCU.buffer.error, MCU.buffer.run, turn_vals);        
      }
      
      //add the forward movement and turn movement
      turn_vals[0] = turn_vals[0] + move_val;
      turn_vals[1] = turn_vals[1] + move_val;
      
      //set the motor speeds
      setLeftSpeed(turn_vals[0]);
      setRightSpeed(turn_vals[1]);
      
      //go to the read state
      state = READ;
    break;
 
    case HEADLESS:
      //turn in random direction (generate random number between 0 and 300 for each motor)
      rand_right = random(0, 300);
      rand_left = random(0,300);

      //set motor speeds
      setLeftSpeed(rand_left);
      setRightSpeed(rand_right);

      //turn for a random amount of time (maybe pick random encoder number?)
      delay(500);

      //move forward at middle speed (150) for both motors
      setLeftSpeed(150);
      setRightSpeed(150);      

      //move for a second or two
      delay(500);
      
      //go back to read state
      state = READ;
    break;    
  } 
}

//TODO: change this to return a value later
//the difference between run and follow is the direction of the motors
uint16_t move_calc(uint16_t error, bool run)
{
  int kp = 1; 
  //check the run bit and determine what to do with the error
  if(run == 1)  
  {
    //TODO: figure out what to change for the error if it is running
  }

  //run proportional controller with error passed in
  int speed = kp * error;
  //caluclate base speed from controller
  return speed;
  //return value calculated
}


//speeds is an array passed in by reference so it can be modifed
void turn_calc(uint16_t error, uint16_t turn, uint16_t &speeds)
{
  int kp = 1;  
  uint16_t speed = 0;

  //run proportional controller with error passed in
  speed = error * kp;
  //check turn bit to determine which motor to apply speeds to
  if(turn == 1)
  {
    //update speed in array passed in
    speeds[0] = speed;
    speeds[1] = 0; //TODO: might change this later
  }  
  else
  {
    //update speed in array passed in
    speeds[0] = 0;
    speeds[1] = speed;
  }
  
}


