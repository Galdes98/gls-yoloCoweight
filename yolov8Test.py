from ultralytics import YOLO

# Create a new YOLO model from scratch
#model = YOLO('yolov8n.yaml')

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8n.pt')

# Train the model using the 'coco128.yaml' dataset for 3 epochs
#results = model.train(data='coco128.yaml', epochs=3)

# Evaluate the model's performance on the validation set
#results = model.val()

# Define path to the image file
#source = 'https://ultralytics.com/images/bus.jpg'
#source = './image0000.jpg'
source = 0

# Perform object detection on an image using the model
#results = model(source)
results = model.predict(source, show=True)

# Export the model to ONNX format
success = model.export(format='onnx')