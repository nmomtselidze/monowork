from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# 1. Setup Model and Pipeline
model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")

# Use a slightly lower temperature for more deterministic, factual medical outputs
generation_config = GenerationConfig(max_new_tokens=250, do_sample=True, temperature=0.1)

def run_agent(system_prompt, user_input):
    """Helper function to route inputs through specific agent personas"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, generation_config=generation_config)
    
    # Extract only the newly generated text response from the chat template
    generated_text = outputs[0]["generated_text"]
    response = generated_text.split("<|im_start|>assistant")[-1].replace("<|im_end|>", "").strip()
    return response

# ==========================================
# PATIENT INPUT
# ==========================================
symptoms = "I have a high fever, dry cough, and severe fatigue."

print("--- Starting Clinical Multi-Agent Pipeline ---\n")

# AGENT 1: The Triage Specialist (Safety Filter)
triage_prompt = (
    "You are an Emergency Medical Triage Specialist. Analyze the user's symptoms. "
    "Identify if there are any immediate life-threatening red flags (e.g., difficulty breathing, chest pain). "
    "Output a brief safety status: either 'CLEAR' or 'EMERGENCY WARNING' with a reason."
)
triage_status = run_agent(triage_prompt, symptoms)
print(f"🚨 [Agent 1: Triage Specialist Status]:\n{triage_status}\n")


# AGENT 2: The Medical Diagnostician
diagnostician_prompt = (
    "You are an Expert Medical Diagnostician. Analyze the patient's symptoms and list the "
    "top 3 most likely medical conditions. For each, provide a 1-sentence clinical reason why."
)
clinical_analysis = run_agent(diagnostician_prompt, symptoms)
print(f"🩺 [Agent 2: Diagnostician Analysis]:\n{clinical_analysis}\n")


# AGENT 3: The Patient Communications Expert (The Final Output Coordinator)
comms_prompt = (
    "You are a compassionate Patient Communications Expert. Take the Triage Status and the Diagnostician Analysis "
    "and synthesize them into a clear, easy-to-read report for the patient. "
    "ALWAYS include a prominent disclaimer that you are an AI, not a doctor, and they should seek professional care."
)
combined_input = f"Patient Symptoms: {symptoms}\nTriage Assessment: {triage_status}\nClinical Analysis: {clinical_analysis}"
final_patient_report = run_agent(comms_prompt, combined_input)

print("📋 [Agent 3: Final Patient Report]:")
print("-" * 40)
print(final_patient_report)
print("-" * 40)
