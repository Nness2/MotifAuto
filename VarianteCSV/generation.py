# -*- coding: <encoding_name> -*-
from PIL import Image
import sys
import cairosvg
import glob
import random
import math
import argparse

def giveColor(image):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_color = (r, g, b)
    for y in range(image.height):
        for x in range(image.width):
            if image.getpixel((x, y)) == (0, 0, 0, 255):
                image.putpixel((x, y), random_color)
    return image

def is_touching(bbox2, Listbbox):

    for bbox1 in Listbbox:
        if bbox1 and bbox2:
            if (bbox1[2] >= bbox2[0] and bbox1[0] <= bbox2[2] and bbox1[3] >= bbox2[1] and bbox1[1] <= bbox2[3]):
                return True

    return False


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


def loadAllMotifs(debug):
    img_list = []
    for filename in glob.glob('Image/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        im = crop_image(im, im.getbbox())
        im = resize_image(im, (1000,1000))
        if debug == True:
            im = giveColor(im)
        img_list.append(im)

    for filename in glob.glob('Image/Normal/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        im = crop_image(im, im.getbbox())
        im = resize_image(im, (700,700))
        if debug == True:
            im = giveColor(im)
        img_list.append(im)

    return img_list


def CreatImagebase(size):
    width = size[0]
    heigth = size[1]
    imageSize = 50
    marge = 0

    widthPortion = width / imageSize
    heigthPortion = heigth / imageSize
    img = Image.new('RGBA', (width, heigth), color='white')
    return img


def PastMotifsOnBase(imageBase, image_list, remplissage):
    listPosition = []
    listRotation = []
    space_taken = []
    suppOffSet = 0.25 #pourcentage de la supperposition

    for i in range(int(1000)):
        # Choose a random small image from the list
        random_number = random.randint(0, len(image_list)-1)

        # Choose a random rotation angle for the small image
        random_rotate = random.randint(0, 360)

        # Rotate the small image by the random angle
        imgRotated = image_list[random_number].rotate(random_rotate, expand=True)
        condition = True;
        greatestImageW = 0
        greatestImageH = 0
        for l in range(len(image_list)):
            if image_list[l].width > greatestImageW:
                greatestImageW = image_list[l].width
            if image_list[l].height > greatestImageH:
                greatestImageH = image_list[l].height

        random_w = random.randint(imageBase.width*remplissage, imageBase.width-(imageBase.width*remplissage)-greatestImageW)
        random_h = random.randint(imageBase.height*remplissage, imageBase.height-(imageBase.height*remplissage)-greatestImageH)

        tryTime = 20000
        break2 = False
        while is_touching((random_w+(imgRotated.width*suppOffSet), random_h+(imgRotated.height*suppOffSet), random_w+imgRotated.width-(imgRotated.width*suppOffSet), random_h+imgRotated.height-(imgRotated.height*suppOffSet)), space_taken):
            tryTime = tryTime-1
            if tryTime <= 0:
                break2 = True
                break
            random_w = random.randint(imageBase.width*remplissage, imageBase.width-(imageBase.width*remplissage)-greatestImageW)
            random_h = random.randint(imageBase.height*remplissage, imageBase.height-(imageBase.height*remplissage)-greatestImageH)

        if break2 == True:
            break2 = False
            break

        #Past the small image
        imgPosition = (random_w, random_h)

        listPosition.append(imgPosition)
        listRotation.append(imgRotated)

        # Store the coordinates of the small image in the list of taken spaces
        space_taken.append((random_w+(imgRotated.width*suppOffSet), random_h+(imgRotated.height*suppOffSet), random_w+imgRotated.width-(imgRotated.width*suppOffSet), random_h+imgRotated.height-(imgRotated.height*suppOffSet)))

    centerx = imageBase.width /2
    centery = imageBase.height /2
    #On colle les images en commencant par les extremiters vers le centre
    while len(listPosition) != 0:
        centerest = 0

        for k in range(len(listPosition)):
            distanceCurrent = math.sqrt((listPosition[centerest][0] - centerx) **2 + (listPosition[centerest][1] - centery) **2)
            distanceNew = math.sqrt((listPosition[k][0] - centerx)**2 + (listPosition[k][1] - centery) **2)
            if(distanceCurrent < distanceNew):
                centerest = k
    
        imageBase.alpha_composite(listRotation[centerest], listPosition[centerest])
        #img.paste(listRotation[centerest], listPosition[centerest])
        del listRotation[centerest]
        del listPosition[centerest]
    return imageBase


def AddImageManually(imgpath, imgDest, position, size, rotation):
    imageload = Image.open(imgpath)
    imageload = resize_image(imageload, size)
    imageload = imageload.rotate(rotation, expand=True)
    imgDest.alpha_composite(imageload, position)




def main(sizeBase, remplissage, DebugColor):
    # Logique principale du script
    remplissage = remplissage / 100
    image_list = loadAllMotifs(DebugColor)

    img = CreatImagebase(sizeBase)
    img = PastMotifsOnBase(img, image_list, remplissage)
    #AddImageManually('mask.png', img, (1000,1000), (1800,1800), 270)
    #AddImageManually('mask.png', img, (200,200), (1800,1800), 90)

    # Afficher l'image
    img.show()
    # Sauvegarder l'image
    img.save('my_image.png', dpi=(300, 300))






if __name__ == '__main__':
    # Appeler la fonction main() si le script est exécuté directement
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, help="largeur image base")
    parser.add_argument("y", type=int, help="hauteur image base")
    parser.add_argument("r", type=int, help="pourcentage de remplissage")
    parser.add_argument("--use-color", action="store_true", help="Utiliser l'option")

    args = parser.parse_args()

    baseSize = (args.x, args.y)
    remplissage = args.r
    main(baseSize, remplissage, args.use_color)