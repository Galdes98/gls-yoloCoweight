from PIL import Image, ImageDraw

def create_line(x1, y1, x2, y2, output_path):
    # Create a blank white image
    image = Image.new('RGB', (max(x1, x2) + 1, max(y1, y2) + 1), 'white')

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Draw the line between the two points
    draw.line([(x1, y1), (x2, y2)], fill='black', width=2)

    # Save the image to the specified output path
    image.save(output_path)

# Example usage:
x1, y1 = 10, 20
x2, y2 = 100, 80
output_path = 'line_image.png'
create_line(x1, y1, x2, y2, output_path)