import transformers

from huggingface_hub.utils import disable_progress_bars
disable_progress_bars()

transformers.logging.set_verbosity_error()
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Load a small language model (e.g., Phi-3 or similar)
model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct" # "microsoft/Phi-3-mini-4k-instruct"  requires HF token
tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")

# Symptom prompt
symptoms = "I have a high fever, dry cough, and severe fatigue."
print("--- Demo Mode: Fallback Response ---")
messages = [
    {"role": "system", "content": "You are a medical AI assistant. Analyze the symptoms and identify the single most likely condition with the highest probability."},
    {"role": "user", "content": symptoms}
]

# Generate Response
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
generation_config = GenerationConfig(max_new_tokens=200, do_sample=True, temperature=0.2)
outputs = pipe(prompt, generation_config=generation_config)
print(outputs[0]["generated_text"])
