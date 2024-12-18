#sudo apt install tesseract-ocr-eng
#pip install pytesseract
#pip install opencv-python

import os
import cv2
import pytesseract

#path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

#tessdata directory
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata'

# Open video capture 
cap = cv2.VideoCapture(0)

# Initialize a string to store recognized text
recognized_sentence = ""

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to detect words and their bounding boxes
    try:
        data = pytesseract.image_to_data(gray, lang="eng", output_type=pytesseract.Output.DICT)
    except pytesseract.TesseractError as e:
        print(f"Error occurred: {e}")
        break

    # Iterate through each word detected by Tesseract
    for i in range(len(data['text'])):
        word = data['text'][i]
        if word.strip():  # Skip empty results
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            # Draw a bounding box around the word
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add word text over the bounding box
            cv2.putText(frame, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            # Append the recognized word 
            recognized_sentence += word + " "

    # Display the recognized sentence
    print("Recognized Sentence:", recognized_sentence.strip())

    # Display the frame with bounding boxes and recognized text
    cv2.imshow('Live OCR with Tesseract', frame)

    # Press 'z' to exit
    if cv2.waitKey(1) & 0xFF == ord('z'):
        break

    # Clear recognized sentence for next frame
    recognized_sentence = ""

cap.release()
cv2.destroyAllWindows()
