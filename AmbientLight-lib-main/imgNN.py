import numpy as np
import cv2
import argparse

#**************************************************
# Title: YOLO Object Detection with OpenCV and Python
# Author: Arun Ponnusamy
# Date: July 16, 2018
# Availability: http://www.arunponnusamy.com
#**************************************************
class Nnimg:
    
    def get_output_layers(self,net):    
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    def tv_detection(self, image) :      
        config = "yolov3.cfg"
        weights = "yolov3.weights"
        classes_inp = "yolov3.txt"
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        classes = None

        with open(classes_inp, 'r') as f:        # r mean readmode -> open the file in readmode, settings for detecting certain objects
            classes = [line.strip() for line in f.readlines()]

        net = cv2.dnn.readNet(weights, config)          
        blob = cv2.dnn.blobFromImage(image, scale, (217,217), (0,0,0), True, crop=False) # detegovany objekt zmenseny na rozmery 416x416
        net.setInput(blob)     
        outs = net.forward(self.get_output_layers(net)) 

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4
      
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:                         # popisuje presnost s akou je objekt detegovany,
                    center_x = int(detection[0] * Width)     # cim blizsie k 0.0, tym je vacsia pravdepodobnost najdenia viacerych objektov, 
                    center_y = int(detection[1] * Height)    # ale aj nepresnych detekcii
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold) # pocet najdenych objektov
        
        for i in indices:  
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            print("NN data x,y,w,h = ",x,y,w,h)
            
            return x,y,w,h
 
            
  
        
