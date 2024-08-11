import pytesseract as tess
import os
from PIL import Image
import cv2
import numpy as np

# Configure Tesseract path
tess_exe_path = os.path.join(os.getcwd(), 'tess', 'tesseract.exe')
tess.pytesseract.tesseract_cmd = tess_exe_path

def img(uploaded_file):
    try:
        # Open the image and convert it for processing
        img = Image.open(uploaded_file)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Apply sharpening filter
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        img_sharp = cv2.filter2D(img, -1, kernel)

        # Convert back to PIL image for Tesseract
        img_pil = Image.fromarray(cv2.cvtColor(img_sharp, cv2.COLOR_BGR2RGB))

        # Extract text using Tesseract
        text = tess.image_to_string(img_pil)

        # Initialize grade and credit lists
        grade = []
        credit = []

        # Define patterns and valid characters
        pf = ["P", "F", "W", "p", "f", "w"]
        grades = [" O ", " A+", " A ", " B+", " B ", " C ", " At", " Bt", " 8 ", " BY", " Be", " at", "ie)", " 0 ", " Q "]
        grades_extra = [' 1a', ' 1b', ' 1c', ' 2a', ' 2b', ' 2c', ' 3a', ' 3b', ' 3c']
        valid_credits = ['1', '2', '3', '4', '5', '0', "8", ")", "|", ".", "y", "a", "0", "Q"]
        valid_credits_simple = ['1', '2', '3', '4', '0', '5']

        # Process the extracted text to identify grades and credits
        l = len(text)
        for i in range(0, l - 3):
            if ((text[i:i + 3] in grades or text[i:i + 3] in grades_extra)) and (
                    (text[i + 4] in pf) or (text[i + 3] in pf) or (text[i + 5] in pf) or (text[i + 6] in pf)):
                
                # Assign the correct grade
                grade_value = text[i:i + 3].strip()
                grade_mapping = {"At": "A+", "Bt": "B+", "BY": "B+", "Be": "B+", "8": "B", "ie)": "O", "0": "O", "Q": "O"}
                grade.append(grade_mapping.get(grade_value, grade_value))

                # Assign the correct credit
                if (text[i - 1]) == ")":
                    credit.append("0")
                elif (text[i - 1]) == "|" or (text[i - 1]) == ".":
                    credit.append(text[i - 3] if text[i - 3] in valid_credits else text[i - 4])
                elif (text[i - 1]) == "8":
                    credit.append("3")
                elif (text[i - 1] == "y"):
                    credit.append("2")
                elif (text[i - 1] in ["a", "Q"]):
                    credit.append("0")
                else:
                    for offset in range(1, 4):
                        if text[i - offset] in valid_credits_simple:
                            credit.append(text[i - offset])
                            break

        return grade, credit

    except Exception as e:
        print(f"Error processing the image: {e}")
        return [], []
