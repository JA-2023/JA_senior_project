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

typedef struct Data
{
  uint8_t turn, direction, move, run, mode;  
  uint8_t turn_error, move_error;
}Data;


/*Code for data struct is sourced and modifed from Pololu ROMIRPiSlaveDemo code*/
PololuRPiSlave<Data,5> MCU;

Romi32U4Motors motors;

void setup() {

  //Set up MCU as I2C peripheral with address of 20
  MCU.init(20);
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);    

}

void loop() {
  uint16_t move_val = 0;
  int16_t turn_vals[2] = {0,0};
  int16_t left_speed = 0;
  int16_t right_speed = 0;
  long rand_left = 0;
  long rand_right = 0;
  switch(state)
  {
    case READ:
      //update buffer to get latest data
      //data sent from pi is stored in the data struct
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
        turn_vals[0] = 0;
        turn_vals[1] = 0;
        move_val = 0;
      }
      
      //calculate the forward movment if the bit is high
      if(MCU.buffer.move == 1) 
      {
        
        move_val = move_calc(MCU.buffer.move_error, MCU.buffer.run);       
        
      }     
      
      //calculate the turn movement if the bit is high
      if(MCU.buffer.turn == 1)
      {
        turn_calc(MCU.buffer.turn_error, MCU.buffer.direction, turn_vals);         
      }
      
      //add the forward movement and turn movement
      left_speed = turn_vals[0] + move_val;
      right_speed = turn_vals[1] + move_val;
      

      //set the motor speeds
      motors.setLeftSpeed(left_speed);
      motors.setRightSpeed(right_speed);
      
      //go to the read state
      state = READ;
    break;
 
    case HEADLESS:
      //turn in random direction (generate random number between 0 and 300 for each motor)
      rand_right = random(0, 300);
      rand_left = random(0,300);

      //set motor speeds
      motors.setLeftSpeed(rand_left);
      motors.setRightSpeed(rand_right);

      //turn for a random amount of time (maybe pick random encoder number?)
      delay(500);

      //move forward at middle speed (150) for both motors
      motors.setLeftSpeed(150);
      motors.setRightSpeed(150);      

      //move for a second or two
      delay(500);
      
      //go back to read state
      state = READ;
    break;    
  } 
}


//the difference between run and follow is the direction of the motors
uint16_t move_calc(uint16_t error, bool run)
{

//TODO: add in run/follow functionality
  
  //values to hold accumulated values for derivative and integral term
  static float d_temp = 0;
  static float i_temp = 0;
  //final speed value
  float speed = 0;


  speed = PID_calc(error,d_temp,i_temp);
  d_temp = error;  

  //return value calculated
  return speed;
}


//speeds is an array passed in by reference so it can be modifed
void turn_calc(uint16_t error, uint16_t direction, uint16_t *speeds)
{
  //values to hold accumulated values for derivative and integral term
  static float d_temp = 0;
  static float i_temp = 0;
  //final speed value
  float speed = 0;

  //accumulate error to get average error (might need to change since there is no negative error)
  //i_temp += error;
  
  speed = PID_calc(error,d_temp,i_temp);
  d_temp = error;  

  //check turn bit to determine which motor to apply speeds to
  if(direction == 1)
  {
    //update speed in array passed in
    speeds[0] = (int16_t)speed;
    speeds[1] = (uint16_t)(-speed); 
  }  
  else
  {
    //update speed in array passed in
    speeds[0] = (uint16_t)(-speed);
    speeds[1] = (int16_t)speed;
  }
  
}

uint16_t PID_calc(uint16_t error, float d_temp, float i_temp)
{
    //Proportional, Integral, and derivative terms
    float P_term;
    float I_term;
    float D_term;  
    //constants for PID calculations
    const float kp = 0.25;  
    const float ki = 0.01;
    const float kd = 0.00;
    //final speed value
    float speed = 0;

    //accumulate error to get average error (might need to change since there is no negative error)
    //i_temp += error;
    

    P_term = kp * error;
    I_term = ki * i_temp;
    D_term = kd * d_temp;  
    //TODO: finish PID code
    speed = P_term + I_term + D_term;

    return speed;
}


