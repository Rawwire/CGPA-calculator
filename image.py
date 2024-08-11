import pytesseract as tess
import os
from PIL import Image
import cv2
import numpy as np

tess_exe_path = "/path/to/tesseract.exe"  # Replace with the actual path
tess.pytesseract.tesseract_cmd = tess_exe_path

def img(uploaded_file):

    img = Image.open(uploaded_file)

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_sharp = cv2.filter2D(img, -1, kernel)


    img_pil = Image.fromarray(cv2.cvtColor(img_sharp, cv2.COLOR_BGR2RGB))

    text = tess.image_to_string(img_pil)
    grade=[]
    credit=[]
    l= len(text)
    pf=["P","F","W","p","f","w"]
    g=[" O ", " A+", " A "," B+"," B ", " C "," At"," Bt"," 8 ", " BY"," Be"," at","ie)"," 0 ", " Q "]
    g1=[" 1a",' 1b',' 1c',' 2a',' 2b',' 2c',' 3a',' 3b',' 3c']
    s=['1','2','3','4','5','0',"8",")","|",".","y","a","0","Q"]
    s1=['1','2','3','4','0','5']
    for i in range(0,l-3):
        if ((text[i:i+3] in g or text[i:i+3] in g1)) and ((text[i+4] in pf) or (text[i+3] in pf) or (text[i+5] in pf) or (text[i+6] in pf)):
            if text[i:i+3]==" At":
                grade.append("A+")
            elif text[i:i+3]==" at":
                grade.append("A+")
            elif (text[i:i+3]==" Bt") or (text[i:i+3]==" BY") or (text[i:i+3]==" Be"):
                grade.append("B+")
            elif text[i:i+3]==" 8 ":
                grade.append("B")
            elif text[i:i+3]=="ie)" or text[i:i+3]==" 0 " or text[i:i+3]==" Q ":
                grade.append("O")
            elif text[i:i+3] in g1:
                grade.append(text[i+2])
                credit.append(text[i+1])
            else:
                grade.append(text[i:i+3])
            if (text[i-1]) in s or (text[i-2]) in s or text[i-3] in s: 
                if (text[i-1])==")":
                    credit.append("0")
                elif (text[i-1])=="|" or (text[i-1])==".":
                    if (text[i-3]) in s :
                        credit.append(text[i-3])
                    elif (text[i-4]) in s :
                        credit.append(text[i-4])
                elif (text[i-1])=="8":
                    credit.append("3")
                elif (text[i-1] == "y"):
                    credit.append("2")
                elif (text[i-1] == "a") or (text[i-1]=="Q"):
                    credit.append("0")
                else:
                    if text[i-1] in s1:
                        credit.append(text[i-1])

                    if text[i-2] in s1:
                        credit.append(text[i-2])

                    if text[i-3] in s1:
                        credit.append(text[i-3])
    return(grade,credit)
