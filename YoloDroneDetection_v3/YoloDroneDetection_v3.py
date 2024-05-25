from ultralytics import YOLO
import serial
import cv2
import math
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())
print(device)
# Load the exported TFLite model
model = YOLO('best_2.pt')
model.to(device)

# # Run inference
# results = tflite_model('C:/drone_detector/test/images/82_JPEG_jpg.rf.507e41c12942df6858f09e30e0525c3b.jpg')

# Run detection on local image
# results = tflite_model(source=0,show=True,conf=0.5, imgsz=1920)

# source from https://dipankarmedh1.medium.com/real-time-object-detection-with-yolo-and-webcam-enhancing-your-computer-vision-skills-861b97c78993


# start webcam
cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1088)
# cap.set(cv2.CAP_PROP_FPS, 90)

# object classes
classNames = ["drone"]
ser = serial.Serial('COM3',9600)

while True:
    success, img = cap.read()
    with torch.cuda.amp.autocast():
        results = model(img, device=device)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # Calculate center coordinates
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            print(center_x)
            print(center_y)

            # Map x-coordinate to servo angle
            print(img.shape[1])
            servo_angle_x = abs(int((center_x / img.shape[1]) * 180)-180)
            servo_angle_y = abs(int((center_y / img.shape[1]) * 180)-180+20)
            print(servo_angle_x)
            print(servo_angle_y)
            # Send servo command to Arduino for horizontal movement
            ser.write(f'{servo_angle_x},{servo_angle_y}\n'.encode())

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls] + str(confidence), org, font, fontScale, color, thickness)


    cv2.imshow('Webcam', img)
    if cv2.waitKey(100) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()