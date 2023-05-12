import cv2
import smbus
import time

#tracker = cv2.TrackerKCF_create()
tracker = cv2.legacy_TrackerMOSSE.create()
#creates deep neural network with the model and config file passed in
dnn_model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                        'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')


#detect an object within the frame then output the bounding box coordinates
def detection(frame):
    #change image size and colors to work with network, then turn into blob
    dnn_model.setInput(cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True))
    #propagate the input forward through the DNN and take the output
    dnn_output = dnn_model.forward()

    box_x = 0
    box_y = 0
    box_width = 0
    box_height = 0

    #get the output data needed
    for detection in dnn_output[0,0,:,:]:
        #get the confidence metric from the ouput
        confidence = detection[2]
        #check if the confidence is above the threshold
        if confidence > .9:

            #get dimensions of the frame (_ holds the color channel, not needed)
            image_height, image_width, _ = frame.shape

            #get the dimensions from the DNN and scale to frame
            box_x = detection[3] * image_width /2
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width /2
            box_height = detection[6] * image_height
    
    return (int(box_x),int(box_y),int(box_width),int(box_height))

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


if __name__ == '__main__':

    test_data = []
    bus = smbus.SMBus(1)
    time.sleep(1)
    
    count = 0
    old_error = 0
    middle = 0
    error = 0
    
    test_data = [no_turn, right,no_move,follow,move_mode,0]
    bus.write_i2c_block_data(20, 0, test_data)

    #set up web camera to get video
    camera = cv2.VideoCapture(0)

    #capture a frame from the camera
    val, frame = camera.read()

    #detect a person from the frame
    bbox = detection(frame=frame)
    #if a person is not found get a new frame and keep trying
    while(bbox == (0,0,0,0)):
        val, frame = camera.read()
        bbox = detection(frame=frame)

    #set up tracker with first frame and bounding box
    good = tracker.init(frame, bbox)
    
    #loop and check read frames
    while True:
        #read new frame
        good, frame = camera.read()

        #check the return value of the camera to check if it works
        if not good:
            break

        #refresh tracker to keep it from getting stuck
        if(count > 10):

            bbox = detection(frame=frame)
            test_data = [no_turn, right,no_move,follow,move_mode,0]
            bus.write_i2c_block_data(20, 0, test_data)
            while(bbox == (0,0,0,0)):
                print("searching")
                val, frame = camera.read()
                bbox = detection(frame=frame)

            tracker = cv2.legacy_TrackerMOSSE.create()
            tracker.init(frame, bbox)
            count = 0
        #update tracker
        else:
            good, bbox = tracker.update(frame)
            
            
        
        #draw new bounding box
        if good:
            
            #calculate the middle of the rectangle
            #get the x coordiante of the box and hen add half of the width
            middle_box = bbox[0] + (bbox[2] / 2)

            #get the dimensions of the fram to dtermine middle
            image_height, image_width, _ = frame.shape

            #get the middle of the frame
            middle_frame = image_width / 2

            #determine direction to spin
            #object is in the right half
            if(middle_box < (middle_frame - 20)):
                #deternmine the error between the middle of the box and frame
               
                error = int(middle_frame - middle_box)
                
                if(error > 300):
                    error = 250

                print(f"left turn error: {error}")  

                test_data = [turn, left, no_move,follow,move_mode,error]

                
            #object is in the left half
            elif((middle_frame + 20) < middle_box):
                
                error = int(middle_box - middle_frame)
                
                if(error > 300):
                    error = 250

                print(f"right turn error: {error}")  

                test_data = [turn, right, no_move,follow,move_mode,error]
                
            #object is within the middle
            else:
                print("middle")
                middle = 1
                error = 0
                test_data = [no_turn, right,no_move,follow,move_mode,0] 
                
        else:
            #tracking failure, try to detect a new person
            print("tracking error")
            error = 0
            test_data = [no_turn, right,no_move,follow,move_mode,0]
            
        try: 
            bus.write_i2c_block_data(20, 0, test_data)
        except:
            print("IO error")
        
        if((error == old_error) and (middle == 0)):
            count += 1
        
        old_error = error
        middle = 0
       # Display result
        #cv2.imshow("Tracking", frame)
        key = cv2.waitKey(3)
        if key == 27:
            break

    #cv2.destroyAllWindows()


