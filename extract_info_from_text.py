from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os

# Load the Hugging Face API key
HUGGING_FACE_KEY = os.environ.get("HUGGING_FACE_KEY")

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct" 
bnb_config = BitsAndBytesConfig(load_in_8bit=True)


tokenizer = AutoTokenizer.from_pretrained(model_name, )
model = AutoModelForCausalLM.from_pretrained(model_name, 
                                             device_map="auto",
                                             quantization_config=bnb_config)

tokenizer.pad_token = tokenizer.eos_token

from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="wrBPPoWVkWeUDucRHf8U"
)

result = CLIENT.infer('/kaggle/input/image-aadhar/aadhar.png', model_id="final-ocr/4")

with open("CLASS_RESULT.txt", "w") as f:
    f.write(result)


