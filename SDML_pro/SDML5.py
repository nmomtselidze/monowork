from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Load a small language model (e.g., Phi-3 or similar)
model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct" # "microsoft/Phi-3-mini-4k-instruct"  requires HF token
tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")

# Travel planning prompt
travel_request = "I need to travel from NY to Madrid. Book tickets on cheap flights for the beginning of October 2026, and order a single room in a hotel not far from metro."
messages = [
    {"role": "system", "content": "You are a travel booking AI assistant. Help with flight bookings, hotel reservations, and travel logistics. Provide practical advice for finding cheap flights and accommodation near public transportation."},
    {"role": "user", "content": travel_request}
]

# Generate Response
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
generation_config = GenerationConfig(max_new_tokens=300, do_sample=True, temperature=0.3)
outputs = pipe(prompt, generation_config=generation_config)
print(outputs[0]["generated_text"])


