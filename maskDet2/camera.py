#Imports for image processing
import cv2
import os
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
 


class VideoCam(object):
    #Load haar cascade
    cascPath = "haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
    mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video_capture.release()

    def get_frame(self):
        # Capture frame-by-frame
        ret, frame = self.video_capture.read()
        #Convert frame to gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Detect face
        faces = self.faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
                                            
        faces_list=[]
        preds=[]
        label=""
        mask = None
        for (x, y, w, h) in faces:
            #Detect face
            face_frame = frame[y:y+h,x:x+w]
            face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
            face_frame = cv2.resize(face_frame, (224, 224))
            face_frame = img_to_array(face_frame)
            face_frame = np.expand_dims(face_frame, axis=0)
            face_frame =  preprocess_input(face_frame)
            faces_list.append(face_frame)
            #increase nose detection accuracy by making the face the region of interest 
            face_frame = frame[y : y + h, x : x + w]
            half_face = frame[y + h//2 + h//5 : y + h, x : x + w]
            resized_frame = cv2.resize(face_frame, (256, 256))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            #detect nose position and mouth position
            nose = self.nose_cascade.detectMultiScale(face_frame, 1.3, 5)
            mouth = self.mouth_cascade.detectMultiScale(half_face, 1.3, 5)
            no_of_noses = len(nose)
            no_of_mouth = len(mouth)
            mask = False
            if (no_of_mouth + no_of_noses == 0):
                label = "Mask"
                mask = True
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "Mask worn! Stay Safe!" if label else "Mask Not Worn Properly! Stay Safe!"
            #Draw a rectangle around face region
            cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)
            text = cv2.putText(frame, label, (x, y- 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            break
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes(), mask
