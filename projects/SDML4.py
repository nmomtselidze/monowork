from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# 1. Setup Model and Pipeline
model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")

generation_config = GenerationConfig(max_new_tokens=300, do_sample=True, temperature=0.3)

def run_agent(system_prompt, user_input):
    """Helper function to simulate an agent call"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, generation_config=generation_config)
    
    # Extract only the newly generated text response
    generated_text = outputs[0]["generated_text"]
    response = generated_text.split("<|im_start|>assistant")[-1].replace("<|im_end|>", "").strip()
    return response

# ==========================================
# TRAVEL QUERY
# ==========================================
travel_query = "I want to visit a warm coastal city in Europe for 7 days in September, I enjoy history, food, and hiking."

print("--- Starting Multi-Agent Execution ---\n")

# AGENT 1: The Destination Scout
scout_prompt = "You are a Destination Scout. Identify the top 3 best-fitting coastal European cities for the user's request. Provide ONLY the names of the cities."
cities_selected = run_agent(scout_prompt, travel_query)
print(f"🤖 [Destination Scout Selected]:\n{cities_selected}\n")

# AGENT 2: The Local Culture & Activity Expert
expert_prompt = "You are a Local Expert. Given a list of cities and user preferences (history, food, hiking), explain briefly what makes each city great for those specific activities."
expert_analysis = run_agent(expert_prompt, f"User Preferences: {travel_query}\nSelected Cities: {cities_selected}")
print(f"🤖 [Local Expert Analysis]:\n{expert_analysis}\n")

# AGENT 3: The Concierge / Final Planner
concierge_prompt = "You are a Master Travel Concierge. Take the expert analysis and construct a high-level 7-day summary itinerary outline choosing the single BEST city from the options."
final_itinerary = run_agent(concierge_prompt, f"Expert Insights: {expert_analysis}")
print(f"🤖 [Final Concierge Itinerary]:\n{final_itinerary}")
