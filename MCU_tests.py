import time
import smbus
#data format is turn, direction, move, run, mode, error

left = 0
right = 1
turn = 1
no_turn = 0
move = 1
no_move = 0
run = 1
follow = 0
move_mode = 1
headless = 0
low_error = 75
high_error = 190

address = 0 #TODO: figure out what to put here 
format = 'hh' #TODO: figure out what to put here

class bot_test():
    def __init__(self) -> None:
        self.test_data = []
        self.bus = smbus.SMBus(1)

    #####follow right turn testing#####
    def test_follow_right(self):
        #turn right, no movement, low error, follow
        self.test_data = [turn, right, no_move,follow,move_mode,low_error]
        
        #send data over I2C
        self.bus.write_i2c_block_data(20, address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, no movement, high error, follow
        self.test_data = [turn, right,no_move,follow,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####follow left turn testing#####
    def test_follow_left(self):
        #turn left, no movement, low error, follow
        self.test_data = [turn, left,no_move,follow,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn left, no movement, high error, follow
        self.test_data = [turn, left,no_move,follow,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####follow movement testing#####
    def test_follow_move(self):
        #no turn, move forward, low error, follow
        self.test_data = [no_turn, left,move,follow,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #no turn, move forward, high error, follow
        self.test_data = [no_turn, left,move,follow,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####follow move and turn testing#####
    def test_follow_move_turn(self):
        #turn left, move forward, low error, follow
        self.test_data = [turn, left,move,follow,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn left, move forward, high error, follow
        self.test_data = [turn, left,move,follow,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, move forward, low error, follow
        self.test_data = [turn, right,move,follow,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, move forward, high error, follow
        self.test_data = [turn, right,move,follow,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####run right turn testing#####
    def test_run_right(self):
        #turn right, no movement, low error, run
        self.test_data = [turn, right,no_move,run,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, no movement, high error, run
        self.test_data = [turn, right,no_move,run,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####run left turn testing#####
    def test_run_left(self):
        #turn left, no movement, low error, run
        self.test_data = [turn, left,no_move,run,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn left, no movement, high error, run
        self.test_data = [turn, left,no_move,run,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####run movement testing#####
    def test_run_move(self):
        #no turn, move forward, low error, run
        self.test_data = [no_turn, left,move,run,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #no turn, move forward, high error, run
        self.test_data = [no_turn, left,move,run,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    #####run move and turn testing#####
    def test_run_move_turn(self):
        #turn left, move forward, low error, run
        self.test_data = [turn, left,move,run,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn left, move forward, high error, run
        self.test_data = [turn, left,move,run,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, move forward, low error, run
        self.test_data = [turn, right,move,run,move_mode,low_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #turn right, move forward, high error, run
        self.test_data = [turn, right,move,run,move_mode,high_error]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

    def test_headless(self):
        self.test_data = [0,0,0,0,headless,0]

        #send data over I2C
        self.bus.write_i2c_block_data(20,address, self.test_data)
        #sleep to observe change
        time.sleep(2)

        #make it so the robot doesn't move
        self.test_data = [no_turn, right,no_move,follow,move_mode,high_error]
        self.bus.write_i2c_block_data(20,address, self.test_data)

if __name__ == "__main__":
    tester = bot_test()

    tester.test_follow_right()
    tester.test_follow_left()
    tester.test_follow_move()
    tester.test_follow_move_turn()

    tester.test_run_left()
    tester.test_run_right()
    tester.test_run_move()
    tester.test_run_move_turn()

    tester.test_headless()
