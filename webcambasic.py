from ultralytics import YOLO
print("we out")

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model

results = model(0, show=True, save=True, conf=.5)
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs