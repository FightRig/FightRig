from ultralytics import YOLO
from functions import waitForCam
import cv2
from datetime import datetime
import sys
print("we out")


def main(headless =False):
    # Load a model
    model = YOLO('yolov8n-pose.pt')  # load an official model

    # Open a connection to the webcam (change the index if you have multiple cameras)
    cap = waitForCam(0)
    prev_time = datetime.now().timestamp()
    framecount = 0
    while True:
        success, frame = cap.read()
        


        # Perform inference on the frame
        results = model(frame)  
        person = results[0].keypoints
        

        
            
        current_time = datetime.now().timestamp()
        delta = current_time - prev_time
        fps = framecount / delta
        success, frame = cap.read()
        framecount += 1
        if framecount % 100 ==0 :
            framecount = 0
            prev_time = current_time

        if not headless:
            cv2.putText(frame, "fps:%.2f"%(fps), (1200, 600), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0, 255))
            cv2.imshow('Webcam', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    headless = "-h" in sys.argv
    main(headless)


