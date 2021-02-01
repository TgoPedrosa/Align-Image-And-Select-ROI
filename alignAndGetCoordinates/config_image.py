# USAGE
# python config_image.py --template data/templatecnh.jpg --image data/testecnh.png

import numpy as np
import cv2
import argparse
from scipy import ndimage
import pytesseract
from align_images import align_images


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="Imagem que será alinhada com o template")
ap.add_argument("-t", "--template", required=True,
	help="Template para fazer o alinhamento")
args = vars(ap.parse_args())

#imagem template
template_img = cv2.imread(args["template"])
input_img = cv2.imread(args["image"])


def ResizeIMG(image):
    
    #calculate the 50 percent of original dimensions
    width = 700
    (h, w) = image.shape[:2]
    r = width / float(w)
    dim = (width, int(h * r))
    # resize image
    image = cv2.resize(image, dim)

    return image

resized_template = ResizeIMG(template_img)
if input_img is not None:
    resized_image = ResizeIMG(input_img)
    final_image = align_images(resized_image, resized_template, debug=True)   
    
else:
    final_image = resized_template  


# REGION OF INTEREST (ROI) SELECTION

# initializing the list for storing the coordinates 
coordinates = [] 
  
# Defining the event listener (callback function)
def shape_selection(event, x, y, flags, param): 
    # making coordinates global
    global coordinates 
  
    # Storing the (x1,y1) coordinates when left mouse button is pressed  
    if event == cv2.EVENT_LBUTTONDOWN: 
        coordinates = [(x, y)] 
  
    # Storing the (x2,y2) coordinates when the left mouse button is released and make a rectangle on the selected region
    elif event == cv2.EVENT_LBUTTONUP: 
        coordinates.append((x, y)) 
  
        # Drawing a rectangle around the region of interest (roi)
        cv2.rectangle(image, coordinates[0], coordinates[1], (0,0,255), 2) 
        cv2.imshow("image", final_image) 
    
  
# load the image, clone it, and setup the mouse callback function 
image = final_image
image_copy = image.copy()
cv2.namedWindow("image") 
cv2.setMouseCallback("image", shape_selection) 
  
  
# keep looping until the 'q' key is pressed 
while True: 
    # display the image and wait for a keypress 
    cv2.imshow("image", image) 
    key = cv2.waitKey(1) & 0xFF
  
    if key==13: # If 'enter' is pressed, apply OCR
        break

    if key == ord("c"): # Clear the selection when 'c' is pressed 
        image = image_copy.copy() 
  
if len(coordinates) == 2: 
    image_roi = image_copy[coordinates[0][1]:coordinates[1][1], 
                               coordinates[0][0]:coordinates[1][0]] 
    cv2.imshow("Selected Region of Interest - Press any key to proceed", image_roi) 
    
    cv2.waitKey(0) 
  
# closing all open windows 
cv2.destroyAllWindows()  
    

#####################################################################################################
# OPTICAL CHARACTER RECOGNITION (OCR) ON ROI
custom_config = r' -l por --oem 1'
text = pytesseract.image_to_string(image_roi,config=custom_config)
print("Text:")
print(text)
print("Coordinates:")
print(coordinates)