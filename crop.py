
from PIL import Image

def is_touching(bbox1, bbox2):

    if (bbox1[2] >= bbox2[0] and bbox1[0] <= bbox2[2] and bbox1[3] >= bbox2[1] and bbox1[1] <= bbox2[3]):
        return True

    return False

# Call the function with the path of your image
print(is_touching((10,10, 15,15),(0,0,20,20)))