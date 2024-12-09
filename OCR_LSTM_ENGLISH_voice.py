import os
import cv2
import pytesseract
from gtts import gTTS
import playsound

# Set the Tesseract executable path (commented out for Linux as it's not needed)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

# Specify the tessdata directory (where your custom model is located)
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata/"'

# Load the input image (replace 'input.jpg' with the path to your image)
image_path = 'C:\\vscode\\ocr_tsting_img.JPG'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Tesseract to detect words and their bounding boxes
try:
    data = pytesseract.image_to_data(gray, lang="eng", config=tessdata_dir_config, output_type=pytesseract.Output.DICT)
except pytesseract.TesseractError as e:
    print(f"Error occurred: {e}")
    exit(1)

# Initialize a string to store the entire recognized sentence
recognized_sentence = ""

# Iterate through each word detected by Tesseract
for i in range(len(data['text'])):
    word = data['text'][i]
    if word.strip():  # Skip empty results
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        # Draw a bounding box around the word
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Put the word text over the bounding box
        cv2.putText(image, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        # Append the recognized word to the sentence string
        recognized_sentence += word + " "

# Display the recognized sentence in the terminal
recognized_sentence = recognized_sentence.strip()
print("Recognized Sentence:", recognized_sentence)

# Display the image with bounding boxes and recognized text
cv2.imshow('OCR Output', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert the recognized sentence to speech
tts = gTTS(text=recognized_sentence, lang='en')
tts.save("C:\\vscode\\output.mp3")

# Play the audio through the Raspberry Pi's audio jack
playsound.playsound("C:\\vscode\\output.mp3")
