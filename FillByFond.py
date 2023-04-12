# -*- coding: <encoding_name> -*-

from PIL import Image
import glob
import random
import math


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

    
def loadAllFond():
    image_listPetit = []
    for filename in glob.glob('Image/Fond/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        image_listPetit.append(im)
    return image_listPetit


def loadAllMotifsMask():
    image_listForm = []
    for filename in glob.glob('Image/Masque/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        im = crop_image(im, im.getbbox())
        image_listForm.append(im)
    return image_listForm

def loadAllMotifsShape():
    image_listForm = []
    for filename in glob.glob('Image/Forme/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        image_listForm.append(im)
    return image_listForm


def PastMotifsOnBase(imageBase, shape):

    for y in range(shape.height):
        for x in range(shape.width):
            if shape.getpixel((x, y))[3] > 0 and shape.getpixel((x, y)) != (255, 0, 0, 255)  and shape.getpixel((x, y)) != (0, 0, 0, 255):
                shape.putpixel((x, y), (0, 0, 0, 255))
    shape.show()

    imageBase.alpha_composite(shape, (0,0))
    for y in range(imageBase.height):
        for x in range(imageBase.width):
            if imageBase.getpixel((x, y)) == (255, 0, 0, 255):
                imageBase.putpixel((x, y), (0, 0, 0, 0))

    imageBase = crop_image(imageBase, shape.getbbox())
    return imageBase





def main():
    image_listFond = loadAllFond()
    image_listShape = loadAllMotifsShape()
    image_listMask = loadAllMotifsMask()
    image_listMask = crop_image(image_listMask[0], image_listShape[0].getbbox())

    imageBase = image_listFond[0]
    shape = image_listMask
    img = PastMotifsOnBase(imageBase, shape)



    # Afficher l'image
    img.show()
    # Sauvegarder l'image
    img.save('outline.png')



if __name__ == '__main__':
    main()