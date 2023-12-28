from ultralytics import YOLO
import cv2

print("we out")

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model

# Open a connection to the webcam (change the index if you have multiple cameras)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Perform inference on the frame
    results = model(frame)  # Adjust size as needed

    for result in results:
        # Extract relevant information
        boxes = result.boxes
        print(dir(boxes))
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs

        # Draw bounding box on the frame
        for box in boxes:
            box = [int(coord) for coord in box.xyxy]
            frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
