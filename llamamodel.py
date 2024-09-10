from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
from extract_text_from_image import extract_from_image


model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct" 
bnb_config = BitsAndBytesConfig(load_in_8bit=True)


tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, 
                                             device_map="auto",
                                            quantization_config=bnb_config)
tokenizer.pad_token = tokenizer.eos_token

with open('systemPrompt.txt', 'r') as f:
    system_prompt_for_aadhar = f.read()



aadhar_from_ocr = """
<s_cord-v2><s_menu><s_nm> GOVERNMENTOEINGIA</s_nm><s_unitprice> </s_unitprice><s_cnt> 3</s_cnt><s_price>name : Gomati</s_price></s_menu><s_sub_total><s_subtotal_price> DOB - 01/05/1993</s_subtotal_price></s_sub_total><s_total><s_total_price> Aadhar number : 345689752341</s_total_price><s_cashprice> 1234</s_cashprice>
</s_total>**&&**
"""

generated_text = extract_from_image("images/aadhar.png")

prompt = f"{system_prompt_for_aadhar}{generated_text}\n\nMedical Report:\n{aadhar_from_ocr}"


inputs = tokenizer(prompt, return_tensors="pt").to("cuda")


output = model.generate(**inputs, max_length=1000, do_sample=True, top_p=0.9)


response = tokenizer.decode(output[0], skip_special_tokens=True)

with open("data.json", 'w') as f:
    f.write(response)
