import pytesseract as tess
import os
from PIL import Image
import cv2
import numpy as np

# Configure Tesseract path based on OS
if os.name == 'nt':  # Windows
    tess_exe_path = os.path.join(os.getcwd(), 'tess', 'tesseract.exe')
else:  # Linux or other OS
    tess_exe_path = '/usr/bin/tesseract'

tess.pytesseract.tesseract_cmd = tess_exe_path

def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_sharp = cv2.filter2D(img, -1, kernel)
    return Image.fromarray(cv2.cvtColor(img_sharp, cv2.COLOR_BGR2RGB))

def extract_text(img_pil):
    try:
        return tess.image_to_string(img_pil)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def parse_grades_and_credits(text):
    grade = []
    credit = []
    pf = ["P", "F", "W", "p", "f", "w"]
    g = [" O ", " A+", " A ", " B+", " B ", " C ", " At", " Bt", " 8 ", " BY", " Be", " at", "ie)", " 0 ", " Q "]
    g1 = [" 1a", ' 1b', ' 1c', ' 2a', ' 2b', ' 2c', ' 3a', ' 3b', ' 3c']
    s = ['1', '2', '3', '4', '5', '0', "8", ")", "|", ".", "y", "a", "0", "Q"]
    s1 = ['1', '2', '3', '4', '0', '5']

    for i in range(0, len(text) - 3):
        if (text[i:i+3] in g or text[i:i+3] in g1) and \
           (text[i+4] in pf or text[i+3] in pf or text[i+5] in pf or text[i+6] in pf):
            if text[i:i+3] == " At" or text[i:i+3] == " at":
                grade.append("A+")
            elif text[i:i+3] in [" Bt", " BY", " Be"]:
                grade.append("B+")
            elif text[i:i+3] == " 8 ":
                grade.append("B")
            elif text[i:i+3] in ["ie)", " 0 ", " Q "]:
                grade.append("O")
            elif text[i:i+3] in g1:
                grade.append(text[i+2])
                credit.append(text[i+1])
            else:
                grade.append(text[i:i+3])

            for j in range(1, 4):
                if text[i-j] in s1:
                    credit.append(text[i-j])
                    break
    return grade, credit

def process_image(uploaded_file):
    img_pil = preprocess_image(uploaded_file)
    text = extract_text(img_pil)
    if text:
        return parse_grades_and_credits(text)
    else:
        return [], []

# Example usage:
# grades, credits = process_image(uploaded_file)
