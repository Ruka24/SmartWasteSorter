# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 22:37:10 2024
@author: Valentina
"""

from cvzone.ClassificationModule import Classifier
import cvzone
import cv2
import os
import threading
import serial  # Import pyserial for communication with Arduino
import time

# Initialize the Arduino serial connection
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port

# Threaded Video Stream Class
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while not self.stopped:
            if self.cap.isOpened():
                self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()


# Initialize the threaded video stream
cap = VideoStream("http://192.168.231.91:8080/video")

# Model and Resources
classifier = Classifier('Resources/Model/keras_model.h5', 'Resources/Model/labels.txt')
imgArrow = cv2.imread('Resources/arrow.png', cv2.IMREAD_UNCHANGED)

# Import all the waste images
imgWasteList = []
pathFolderWaste = "Resources/Waste"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

# Import all the bin images
imgBinsList = []
pathFolderBins = "Resources/Bins"
pathList = os.listdir(pathFolderBins)
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

# Classification dictionary
classDic = {
    1: 1,
    2: 1,
    3: 4,
    4: 4,
    5: 2,
    6: 2,
    7: 3,
    8: 3
}

frame_counter = 0
current_bin = -1  # Track the currently open bin
last_detected_id = None  # Track the last detected class ID
consecutive_count = 0  # Count consecutive frames with the same ID
stabilization_threshold = 3  # Number of consecutive frames needed to stabilize


# Function to send class ID to Arduino
def send_to_arduino(class_id):
    global current_bin
    if class_id != current_bin:  # Only send if there's a change
        try:
            arduino.write(f"{class_id}\n".encode())
            print(f"Sent to Arduino: {class_id}")
            current_bin = class_id  # Update the currently open bin

            if class_id != -1:  # If not closing all bins
                time.sleep(5)  # Adjust the delay as needed
        except Exception as e:
            print(f"Error sending data to Arduino: {e}")


# Main loop
while True:
    # Read frame from the video stream
    ret, img = cap.read()
    if not ret:
        print("Failed to capture image from the camera.")
        continue

    # Process every 5th frame to reduce workload
    frame_counter += 1
    if frame_counter % 5 != 0:
        continue

    # Resize the image to the required dimensions
    imgResize = cv2.resize(img, (591, 376))
    imgBackground = cv2.imread('Resources/background.png')

    # Run the classifier prediction on every 5th frame
    prediction = classifier.getPrediction(img)
    classID = prediction[1]
    print(f"Class ID: {classID}")

    # Check if the detected class is valid
    if classID in classDic:
        classIDBin = classDic[classID]

        # Check if the detection is stable
        if classID == last_detected_id:
            consecutive_count += 1
        else:
            consecutive_count = 1  # Reset count for a new ID
            last_detected_id = classID

        # Open the bin only if the detection is stable
        if consecutive_count >= stabilization_threshold:
            send_to_arduino(classIDBin)
            # Overlay waste and bin images
            imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (1030, 150))
            imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (1080, 340))
            imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classIDBin - 1], (1000, 400))
    else:
        print(f"Unexpected Class ID: {classID}")  # Debug message for invalid class IDs
        send_to_arduino(-1)  # Default action: Close all bins

    # Insert resized video feed into background image
    imgBackground[38:38 + 376, 160:160 + 591] = imgResize

    # Display the output
    cv2.imshow("Waste Sorter", imgBackground)

    # Break on pressing '1'
    if cv2.waitKey(10) == ord('1'):
        break

# Cleanup
cap.stop()
arduino.close()
cv2.destroyAllWindows()
