import cv2

# Pretrained classes in the model
# classNames = {0: 'background',
#               1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
#               7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
#               13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
#               18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
#               24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
#               32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
#               37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
#               41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
#               46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
#               51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
#               56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
#               61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
#               67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
#               75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
#               80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
#               86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
classNames = {0: 'background',1: 'person'}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

def main():
    #creates deep neural network with the model and config file passed in
    dnn_model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                              'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
    
    #capture video from webcamera
    vid = cv2.VideoCapture(0)
    while True:
        #read image from the camera
        ret, frame = vid.read()
        #change image size and colors to work with network, then turn into blob
        dnn_model.setInput(cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True))
        #propagate the input forward through the DNN and take the output
        dnn_output = dnn_model.forward()
        
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
                box_x = detection[3] * image_width
                box_y = detection[4] * image_height
                box_width = detection[5] * image_width
                box_height = detection[6] * image_height

                #draw box on image
                cv2.putText(frame, class_name,(int(box_x), int(box_y+0.05* image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0,0,255))
                cv2.rectangle(frame, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23,230,210), thickness=2)
        

        

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(30)
        if key == 27:
            break

    cv2.destroyAllWindows()

    

if __name__ == '__main__':
    main()