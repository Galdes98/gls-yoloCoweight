from roboflow import Roboflow
from PIL import Image, ImageDraw

rf = Roboflow(api_key="3E7t3sq8f4V5liAfrAtD")
project = rf.workspace().project("coweight")
model = project.version(2).model

# infer on a local image
modelJson = model.predict("cows.jpg").json()
#print(modelJson)

# infer on an image hosted elsewhere
#print(model.predict("URL_OF_YOUR_IMAGE").json())

# save an image annotated with your predictions
model.predict("cows.jpg").save("prediction.jpg")

im = Image.open("prediction.jpg")
print(im.format, im.size, im.mode)
#im.show()

#im = im.convert("L")
#im.show()

#print(modelJson['predictions'][0])

# Set the color and size of the points
point_color = (255, 255, 0)  # Black color
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
    draw.polygon(polygon_points, fill=fill_color, outline=fill_color)     

# Display the image
im.show()