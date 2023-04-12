# -*- coding: <encoding_name> -*-
from PIL import Image
import glob
import random
import math
import copy


def detect_pixel(image):
    im = image
    listPoint = []
    pixels = im.load()
    for i in range(1, im.width-1):
        for j in range(im.height-1):
            #print(pixels[i, j])
            if pixels[i, j] == (0, 0, 0, 255) and pixels[i-1, j][3] < 200 or pixels[i-1, j] == (0, 0, 0) and pixels[i, j][3] < 10:
                listPoint.append((i, j, 90))

            if pixels[i, j] == (0, 0, 0, 255) and pixels[i+1, j][3] < 200 or pixels[i+1, j] == (0, 0, 0) and pixels[i, j][3] < 10:
                listPoint.append((i, j, -90))

            if pixels[i, j] == (0, 0, 0, 255) and pixels[i, j-1][3] < 200 or pixels[i, j-1] == (0, 0, 0) and pixels[i, j][3] < 10:
                listPoint.append((i, j, 0))

            if pixels[i, j] == (0, 0, 0, 255) and pixels[i, j+1][3] < 200 or pixels[i, j+1] == (0, 0, 0) and pixels[i, j][3] < 10:
                listPoint.append((i, j, 180))

    return listPoint


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

    
def loadAllMotifsPetit():
    image_listPetit = []
    for filename in glob.glob('Image/Tetes/*.png'): #assuming png
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


#img = image_listForm[0]
def CreatImagebase(list_form):
    img = list_form[0]
    return img


def PastMotifsOnBase(imageBase, image_list):
    listPosition = []
    listRotation = []
    space_taken = []
    test = detect_pixel(imageBase) #Contient tout les positions sur la ligne detecté

    randomPos = []

    while (len(randomPos) < 10):
        im = image_list[random.randint(0, len(image_list)-1)]
        pos = random.randint(0, len(test)) #Prend une position sur la ligne au hasard
        if is_touching((test[pos][0]-int(im.width/2), test[pos][1]-int(im.height/2), test[pos][0]+int(im.width/2), test[pos][1]+int(im.height/2)), space_taken) == False:
            randomPos.append(pos)
    
            w = im.width
            h = im.height
            midle_w = test[pos][0]-int(w/2)
            midle_h = test[pos][1]-int(h/2)
            ime = image_list[random.randint(0, len(image_list)-1)].rotate(test[pos][2], expand=True)

            listPosition.append((midle_w, midle_h))
            listRotation.append(ime)
            space_taken.append((midle_w-(im.width/2), midle_h-(im.height/2), midle_w+(im.width/2), midle_h+(im.height/2)))
    

    while len(listPosition) != 0:
        for k in range(len(listPosition)):
            imageBase.alpha_composite(listRotation[0], listPosition[0])
            del listRotation[0]
            del listPosition[0]

    return imageBase


def main():
    image_listForm = loadAllMotifsForm()
    image_listPetit = loadAllMotifsPetit()

    lastMask = copy.copy(image_listForm[0])

    img = CreatImagebase(image_listForm)

    #img = PastMotifsOnBase(img, image_listPetit)
    #for i in range(len(test)):
    #    img.putpixel((test[i][0], test[i][1]), (255, 0, 0, 255))

    img = PastMotifsOnBase(image_listForm[0], image_listPetit)

    lastMask = crop_image(lastMask, img.getbbox())
    img = crop_image(img, img.getbbox())
    img.alpha_composite(lastMask, (0,0))
    
    # Afficher l'image
    img.show()
    # Sauvegarder l'image
    img.save('outline.png')



if __name__ == '__main__':
    main()