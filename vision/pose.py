from ultralytics import YOLO
from functions import waitForCam
import cv2
from datetime import datetime
import torch
import sys
print("we out")

def main(model, headless =False,):
    cap = waitForCam(0)
    prev_time = datetime.now().timestamp()
    framecount = 0  
    while True:
        success, frame = cap.read()

        # Perform inference on the frame
        results = model(frame, show=True)  
        points = results[0].keypoints[0].xy[0]

        for idx, kpt in enumerate(points):
            coord = list(map(int, kpt))
            print(f"Keypoint {idx}: ({coord[0]}, {coord[1]})")
            cv2.putText(frame, f"{idx}:({int(kpt[0])}, {int(kpt[1])})", (int(kpt[0]), int(kpt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

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
    device = 0 if torch.cuda.is_available() else "cpu"
    if device == 0:
        torch.cuda.set_device(0)
    model = YOLO('yolov8n-pose.pt')
    model.to("cuda")
    print("Model loaded. Using deivce: ", model.device.type)
    main(model, headless)


