from PIL import Image

image = Image.open("path/to/your/image.jpg")

ppi = 300  # Replace with the actual PPI of your image or display
ppc = 1 / 2.54  # Pixels per centimeter, assuming 1 inch is equal to 2.54 centimeters
conversion_factor = ppi * ppc

pixel_measurement = 100  # Replace with the actual pixel measurement
centimeters = pixel_measurement / conversion_factor
print("Length in centimeters:", centimeters)