from roboflow import Roboflow
from PIL import Image, ImageDraw
import numpy as np

rf = Roboflow(api_key="3E7t3sq8f4V5liAfrAtD")
project = rf.workspace().project("coweight")
model = project.version(2).model

# infer on a local image
modelJson = model.predict("BLF2119_15.jpg").json()
#print(modelJson)

# infer on an image hosted elsewhere
#print(model.predict("URL_OF_YOUR_IMAGE").json())

# save an image annotated with your predictions
model.predict("BLF2119_15.jpg").save("prediction_profile.jpg")

im = Image.open("prediction_profile.jpg")
# Get the metadata of the image
metadata = im.info
print(metadata)
print(im.format, im.size, im.mode)

# Get the resolution of the image
resolution = metadata.get('dpi')

# Display the resolution
print(f"Resolution: {resolution} pixels per inch")

# Get the resolution of the image
resolution = metadata.get('dpi')

#im = im.convert("L")
#print(modelJson['predictions'][0])

# Set the color and size of the points
point_color = (255, 255, 0)  # Yellow color
point_size = 2

# Set the fill color for the polygons
fill_color = (255, 255, 0)  # Yellow color

# Create a drawing object
draw = ImageDraw.Draw(im)

# Loop to draw the points
for i in modelJson['predictions']:
    polygon_points = []
    #print (i['x'], i['y'])    
    x_old, y_old = None, None
    for n in i['points']:
        #print (n['x'], n['y'])
        x, y = n['x'], n['y']
        polygon_points.append((x, y))
        draw.ellipse((x - point_size, y - point_size, x + point_size, y + point_size), fill=point_color)
        if 'x_old' in locals() and 'y_old' in locals() and x_old is not None and y_old is not None:
            draw.line([(x_old, y_old), (x, y)], fill=point_color, width=4)
        x_old, y_old = x, y
    #draw.polygon(polygon_points, fill=fill_color, outline=fill_color)     

# Create a mask of the polygon
mask = Image.new('L', im.size, 0)
ImageDraw.Draw(mask).polygon(polygon_points, outline=1, fill=1)
mask = np.array(mask)

# Calculate the width and height inside the polygon in pixels
width_pixels = np.sum(mask, axis=1).max() - np.sum(mask, axis=1).min()
height_pixels = np.sum(mask, axis=0).max() - np.sum(mask, axis=0).min()

# Calculate the resolution in pixels per centimeter
sensor_size = 1/2.0 * 2.54 # Sensor size in inches to centimiters
distance = 170 # Distance from the camera to the object in centimeters
image_width_pixels, image_height_pixels = im.size
resolution = (sensor_size * distance) / max(image_width_pixels, image_height_pixels)
#resolution = 0.25344541484716157205240174672489
print (width_pixels)
print (height_pixels)
print (resolution)

# Convert the width and height from pixels to centimeters
width_cm = width_pixels * resolution
height_cm = height_pixels * resolution

# Display the width and height in centimeters
print(f"Width inside polygon: {width_cm:.2f} cm")
print(f"Height inside polygon: {height_cm:.2f} cm")

# Calculate the distance between each pair of adjacent points in the polygon in centimeters
distances_cm = []
for i in range(len(polygon_points)):
    x1, y1 = polygon_points[i]
    x2, y2 = polygon_points[(i + 1) % len(polygon_points)]
    distance_pixels = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    distance_cm = distance_pixels * resolution
    distances_cm.append(distance_cm)

tot_dist_cm = 0

# Display the distances between each pair of adjacent points in the polygon in centimeters
for i, distance_cm in enumerate(distances_cm):
    #print(f"Distance between points {i} and {i+1}: {distance_cm:.2f} cm")
    tot_dist_cm = tot_dist_cm + distance_cm

print(f"Total distance between points: {tot_dist_cm:.2f} cm")

# calculate the weight
weight = -413.36 + (2.69 * (tot_dist_cm * 0.85)) + (1.50 * tot_dist_cm)
print(f"Weight of the cow: {weight:.2f} Kg")

# Display the image
im.show()