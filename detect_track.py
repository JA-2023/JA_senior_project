import cv2

classNames = {0: 'background',1: 'person'}

tracker_types = ['KCF', 'MOSSE']

tracker_type = tracker_types[1]

    
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
    
    
if tracker_type == 'MOSSE':
    tracker = cv2.legacy_TrackerMOSSE.create()
    

    

#creates deep neural network with the model and config file passed in
dnn_model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                        'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')



def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

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
            class_id = detection[1]
            class_name = id_class_name(class_id,classNames)
            #create the bounding box

            #get dimensions of the frame (_ holds the color channel, not needed)
            image_height, image_width, _ = frame.shape

            #get the dimensions from the DNN and scale to frame
            box_x = detection[3] * image_width * .8
            box_y = detection[4] * image_height 
            box_width = detection[5] * image_width * .8
            box_height = detection[6] * image_height 
    
    return (int(box_x),int(box_y),int(box_width),int(box_height))


def tracking(camera, frame, bbox):

    #set up tracker with first frame and bounding box
    good = tracker.init(frame, bbox)
    
    #loop and check read frames
    while True:
        #read new frame
        good, frame = camera.read()

        #check the return value of the camera to check if it works
        if not good:
            break

        #update tracker
        good, bbox = tracker.update(frame)

        #draw new bounding box
        if good:
            #if tracking worked then get the bound box values and make a rectangle
            point1 = (int(bbox[0]), int(bbox[1]))
            point2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, point1, point2, (255,0,0), 2, 1)
        else:
            #tracking failure, try to detect a new person
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

         # Display result
        cv2.imshow("Tracking", frame)
        key = cv2.waitKey(30)
        if key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    count = 0
    #set up web camera to get video
    camera = cv2.VideoCapture(0)

    #capture a frame from the camera
    val, frame = camera.read()

    #detect a person from the frame
    bbox = detection(frame=frame)
    #if a person is not found then keep trying
    while(bbox == (0,0,0,0)):
        val, frame = camera.read()
        bbox = detection(frame=frame)

    #set up tracker with first frame and bounding box
    good = tracker.init(frame, bbox)
    
    #loop and check read frames
    while True:
        #read new frame
        good, frame = camera.read()

        # Start timer
        timer = cv2.getTickCount()
        

        #check the return value of the camera to check if it works
        if not good:
            break

        #refresh tracker to keep it from getting stuck
        if(count > 30):

            bbox = detection(frame=frame)

            while(bbox == (0,0,0,0)):
                val, frame = camera.read()
                bbox = detection(frame=frame)

            tracker = cv2.legacy_TrackerMOSSE.create()
            tracker.init(frame, bbox)
            count = 0
        #update tracker
        else:
            good, bbox = tracker.update(frame)
            count += 1
        
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        #draw new bounding box
        if good:
            #if tracking worked then get the bound box values and make a rectangle
            point1 = (int(bbox[0]), int(bbox[1]))
            point2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, point1, point2, (255,0,0), 2, 1)

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
                cv2.putText(frame, "Turn left", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

                #deternmine the error between the middle of the box and frame
                error = middle_frame - middle_box
                print(f"left turn error: {error}")   

                
            #object is in the left half
            elif((middle_frame + 20) < middle_box):
                cv2.putText(frame, "Turn right", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                error = middle_box - middle_frame
                print(f"right turn error: {error}")   
                
            #object is within the middle
            else:
                cv2.putText(frame, "middle", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                
        else:
            #tracking failure, try to detect a new person
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            
        
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        #cv2.putText(frame, "object",(int(bbox[0]), int(bbox[1]+0.05* bbox[3])),cv2.FONT_HERSHEY_SIMPLEX,(.005*bbox[2]),(0,0,255))
        
        
            
         # Display result
        cv2.imshow("Tracking", frame)
        key = cv2.waitKey(30)
        if key == 27:
            break

    cv2.destroyAllWindows()


