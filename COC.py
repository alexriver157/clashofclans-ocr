from PIL import Image, ImageGrab
import pytesseract
import cv2 
import numpy as np
import time
import pyautogui, random
ps = mr = er = 0
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

#Minimum of each resource
quant = 800000
#Coords of resources
#loc down, loc left, width, height
ssreg = (167, 206, 357, 317)

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 220, 255, 0)[1]

while True:  
    time.sleep(random.randint(2, 5))
    img = thresholding(get_grayscale(np.array(ImageGrab.grab(ssreg))))
    Image.fromarray(img).save("img.png")
    try:
        txt = pytesseract.image_to_string(img, config=custom_config)
        vals = txt.split("\n", 1)
        for i, s in enumerate(vals):
            vals[i]=int(''.join(e for e in s if e.isalnum()))
        if any(y > 2000000 for y in vals) or any(y <10000 for y in vals):
            print("misread", vals)
            mr += 1
        elif (vals[0] > quant and vals[1] > quant) or ((vals[0] - quant + vals[1]) > (quant *1.2)):
            print("Attack,", vals)
            print (f"Total Passes: {ps}\nTotal Erors: {er}\nTotal Misreads: {mr}")
            input()
            pyautogui.click(random.randint(2100, 2150), random.randint(920, 970))
        else:
            print("pass", vals)
            ps += 1
            #Coords of continue button, randomized to avoid ban
            pyautogui.click(random.randint(2100, 2150), random.randint(920, 970))
    except Exception as e:
        print(e)
        print("Base values not loaded/not detected", vals)
        er += 1