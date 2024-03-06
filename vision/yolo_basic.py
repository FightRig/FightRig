from ultralytics import YOLO
import torch

print("we out")

device = 0 if torch.cuda.is_available() else "cpu"
if device == 0:
    torch.cuda.set_device(0)
print(device)
# Load a model
model = YOLO('yolov8n-pose.pt', device)  # load an official model
model.to("cuda")
print(model.device.type)

results = model(0, show=True, save=True, conf=.5)
print(model.device.type)
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs