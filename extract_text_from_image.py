from transformers import AutoTokenizer,  VisionEncoderDecoderModel, AutoProcessor
import torch
import cv2
import pytesseract

tokenizer = AutoTokenizer.from_pretrained("jinhybr/OCR-Donut-CORD")

model = VisionEncoderDecoderModel.from_pretrained("jinhybr/OCR-Donut-CORD")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Automatically select GPU if available
model = model.to(device) 

# Displaying image
from PIL import Image
import torch
import matplotlib.pyplot as plt


def extract_from_image(image_path):
    
    image = Image.open(image_path).convert("RGB")
    processor = AutoProcessor.from_pretrained("jinhybr/OCR-Donut-CORD")

    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device) 

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]


    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image)

    whole_text = f"{generated_text} {extracted_text}"

    return whole_text
