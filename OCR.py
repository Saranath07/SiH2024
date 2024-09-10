import os
import pytesseract
from PIL import Image

data_dir = 'data'
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
if not os.path.exists(data_dir):
    print(f"Directory '{data_dir}' not found.")
    exit()

for filename in os.listdir(data_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        image_path = os.path.join(data_dir, filename)
        print(f"Processing {image_path}")

        try:
            image = Image.open(image_path)
            gray_image = image.convert('L')
            extracted_text = pytesseract.image_to_string(gray_image)
            text_file_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}.txt')
            with open(text_file_path, 'w') as text_file:
                text_file.write(extracted_text)

            print(f"Extracted text from {filename} and saved to {text_file_path}")

        except Exception as e:
            print(f"Failed to process {image_path} due to error: {e}")

print("Processing completed.")
