from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Load a small language model (e.g., Phi-3 or similar)
model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct" # "microsoft/Phi-3-mini-4k-instruct"  requires HF token
tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")

# Travel prompt
travel_query = "I want to visit a warm coastal city in Europe for 7 days in September, I enjoy history, food, and hiking."
messages = [
    {"role": "system", "content": "You are a travel planning assistant. Based on the traveler's preferences, suggest the top 3 destination cities with a brief reason for each."},
    {"role": "user", "content": travel_query}
]

# Generate Response
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
generation_config = GenerationConfig(max_new_tokens=200, do_sample=True, temperature=0.2)
outputs = pipe(prompt, generation_config=generation_config)
print(outputs[0]["generated_text"])
