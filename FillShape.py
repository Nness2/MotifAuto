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

    
def loadAllMotifsPetit():
    image_listPetit = []
    for filename in glob.glob('Image/Petit/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        im = crop_image(im, im.getbbox())
        im = resize_image(im, (100,100))
        image_listPetit.append(im)
    return image_listPetit


def loadAllMotifsForm():
    image_listForm = []
    for filename in glob.glob('Image/Forme/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        #im = resize_image(im, (2000,2000))
        image_listForm.append(im)
    return image_listForm


def loadAllMotifsMask():
    image_listMask = []
    for filename in glob.glob('Image/Masque/*.png'): #assuming png
        im=Image.open(filename)
        im = im.convert("RGBA")
        #im = resize_image(im, (2000,2000))
        image_listMask.append(im)
    return image_listMask



#img = image_listForm[0]
def CreatImagebase(list_form):
    img = crop_image(list_form[0], list_form[0].getbbox())
    return img

def CreatMaskbase(list_mask, list_form):
    msk = crop_image(list_mask[0], list_form[0].getbbox())
    width, height = msk.size
    for y in range(height):
        for x in range(width):
            if msk.getpixel((x, y))[3] > 0 and msk.getpixel((x, y)) != (255, 0, 0, 255)  and msk.getpixel((x, y)) != (0, 0, 0, 255):
                msk.putpixel((x, y), (0, 0, 0, 255))
    return msk





def is_touching(bbox2, Listbbox):
    for bbox1 in Listbbox:
        if bbox1 and bbox2:
            if (bbox1[2] >= bbox2[0] and bbox1[0] <= bbox2[2] and bbox1[3] >= bbox2[1] and bbox1[1] <= bbox2[3]):
                return True
    return False


def PastMotifsOnBase(imageBase, image_list, mask):
    listPosition = []
    listRotation = []
    space_taken = []
    suppOffSet = 0.25

    for i in range(int(50000)):
        # Choose a random small image from the list
        random_number = random.randint(0, len(image_list)-1)
        # Choose a random position for the small image
        random_w = random.randint(0, imageBase.width)
        random_h = random.randint(0, imageBase.height)

        # Choose a random rotation angle for the small image
        random_rotate = random.randint(0, 360)

        # Rotate the small image by the random angle
        imgRotated = image_list[random_number].rotate(random_rotate, expand=True)
        imgRotated = crop_image(imgRotated, imgRotated.getbbox())

        random_w = random.randint(0, imageBase.width)
        random_h = random.randint(0, imageBase.height)

        tryTime = 20000
        break2 = False
        while is_touching((random_w+(imgRotated.width*suppOffSet), random_h+(imgRotated.height*suppOffSet), random_w+imgRotated.width-(imgRotated.width*suppOffSet), random_h+imgRotated.height-(imgRotated.height*suppOffSet)), space_taken):
            tryTime = tryTime-1
            if tryTime <= 0:
                break2 = True
                break
            random_w = random.randint(0, imageBase.width)
            random_h = random.randint(0, imageBase.height)

        if break2 == True:
            break2 = False
            break

        #Past the small image
        #img.paste(imgRotated, (random_w, random_h))
        imgPosition = (random_w, random_h)
        #img.paste(image_list[random_number], (int(50*i), int(50*j)))

        listPosition.append(imgPosition)
        listRotation.append(imgRotated)
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
        del space_taken[centerest]
    imageBase.alpha_composite(mask, (0,0))

    for y in range(imageBase.height):
        for x in range(imageBase.width):
            # Get the color of the pixel at (x, y) coordinates
            if imageBase.getpixel((x, y)) == (255, 0, 0, 255):
                imageBase.putpixel((x, y), (0, 0, 0, 0))
    
    return imageBase





def main():
    image_listForm = loadAllMotifsForm()
    image_listMask = loadAllMotifsMask()
    image_listPetit = loadAllMotifsPetit()

    img = CreatImagebase(image_listForm)
    mask = CreatMaskbase(image_listMask, image_listForm)
    img = PastMotifsOnBase(img, image_listPetit, mask)

    # Afficher l'image
    img.show()
    # Sauvegarder l'image
    img.save('mask.png')



if __name__ == '__main__':
    main()