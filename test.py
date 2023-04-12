# -*- coding: <encoding_name> -*-

from PIL import Image
import glob
import random
import math
from PIL import Image, ImageOps

width = 500
heigth = 500


def resize_image(image1, new_size):
    # Open the image
    img = image1

    # Calculate the aspect ratio of the image
    width, height = img.size
    aspect_ratio = width / height

    # Calculate the new height based on the aspect ratio and the new width
    new_width, new_height = new_size
    new_height = int(new_width / aspect_ratio)

    # Resize the image
    resized_img = img.resize((new_width, new_height))

    # Display the resized image
    return resized_img


def crop_image(image1, bbox):
    return image1.crop(bbox)


image_list = []
for filename in glob.glob('Image/*.png'): #assuming png
    im=Image.open(filename)
    im = im.convert("RGBA")
    im = crop_image(im, im.getbbox())
    image_list.append(im)

image_list[0].show()

im = resize_image(image_list[0], (210,210))
im.show()

for y in range(im.height):
    for x in range(im.width):
        if im.getpixel((x, y))[3] < 255:
            im.putpixel((x, y), (0, 0, 0, 255))

im.show()


img.save('my_image.png', dpi=(300, 300))
#img.show()
