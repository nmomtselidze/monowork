(venv) user@user:/media/user/dsk64/Multi_ADK$ python
Python 3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
>>> 
>>> # Load a small language model (e.g., Phi-3 or similar)
>>> model_id = "microsoft/Phi-3-mini-4k-instruct"
>>> tokenizer = AutoTokenizer.from_pretrained(model_id)
config.json: 100%|██████████████████████████████| 967/967 [00:00<00:00, 793kB/s]
tokenizer_config.json: 3.44kB [00:00, 2.36MB/s]
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
tokenizer.json: 1.94MB [00:00, 11.9MB/s]
tokenizer.model: 100%|████████████████████████████████████████████████████████████████| 500k/500k [00:01<00:00, 358kB/s]
added_tokens.json: 100%|████████████████████████████████████████████████████████████████| 306/306 [00:00<00:00, 334kB/s]
special_tokens_map.json: 100%|██████████████████████████████████████████████████████████| 599/599 [00:00<00:00, 924kB/s]
>>> pipe = pipeline("text-generation", model=model_id, tokenizer=tokenizer, device_map="auto")
model.safetensors.index.json: 16.5kB [00:00, 44.7MB/s]
Downloading (incomplete total...):   2%|▋                                         | 134M/7.64G [01:58<1:49:50, 1.14MB/s]
Fetching 2 files: 100%|██████████████████████████████████████████████████████████████████| 2/2 [10:34<00:00, 317.37s/it]
Download complete: 100%|███████████████████████████████████████████████████████████| 7.64G/7.64G [10:34<00:00, 12.0MB/s]
Loading weights: 100%|██████████████████████████████████████████████████████████████| 195/195 [00:00<00:00, 4130.04it/s]
generation_config.json: 100%|███████████████████████████████████████████████████████████| 181/181 [00:00<00:00, 553kB/s]
>>> 
>>> # Symptom prompt
>>> symptoms = "I have a high fever, dry cough, and severe fatigue."
>>> messages = [
...     {"role": "system", "content": "You are a medical AI assistant. Analyze the symptoms and list the top 3 potential conditions."},
...     {"role": "user", "content": symptoms}
... ]
>>> 
>>> # Generate Response
>>> prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
>>> outputs = pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.2)
[transformers] Passing `generation_config` together with generation-related arguments=({'max_new_tokens', 'temperature', 'do_sample'}) is deprecated and will be removed in future versions. Please pass either a `generation_config` object OR all generation parameters explicitly, but not both.
[transformers] Both `max_new_tokens` (=200) and `max_length`(=20) seem to have been set. `max_new_tokens` will take precedence. Please refer to the documentation for more information. (https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)
[transformers] Ignoring clean_up_tokenization_spaces=True for BPE tokenizer TokenizersBackend. The clean_up_tokenization post-processing step is designed for WordPiece tokenizers and is destructive for BPE (it strips spaces before punctuation). Set clean_up_tokenization_spaces=False to suppress this warning, or set clean_up_tokenization_spaces_for_bpe_even_though_it_will_corrupt_output=True to force cleanup anyway.
>>> print(outputs[0]["generated_text"])
<|system|>
You are a medical AI assistant. Analyze the symptoms and list the top 3 potential conditions.<|end|>
<|user|>
I have a high fever, dry cough, and severe fatigue.<|end|>
<|assistant|>
 Based on the symptoms of high fever, dry cough, and severe fatigue, the top three potential conditions could be:

1. Influenza (Flu): The flu is a viral infection that affects the respiratory system, causing symptoms such as fever, cough, and fatigue. 
It is highly contagious and can be prevented with annual vaccination.

2. COVID-19: This is a viral infection caused by the SARS-CoV-2 virus. It shares many symptoms with the flu, including fever, cough, and fatigue. 
COVID-19 can range from mild to severe and can be prevented with vaccination and other preventive measures.

3. Pneumonia: This is an infection that inflames the air sacs in one or both lungs, which can fill with fluid or pus. It
>>> 

#========================================================
SDML0.py is a minimal medical symptom analysis script using a small local LLM. Here's how it works:

1. Model loading (lines 1–6)

Loads HuggingFaceTB/SmolLM2-1.7B-Instruct — a compact 1.7B instruction-tuned model
Creates a tokenizer (with BPE-safe settings) and a text-generation pipeline that auto-selects CPU/GPU
2. Prompt construction (lines 8–13)

Defines a hardcoded symptom string
Builds a chat-style message list with:
A system prompt telling the model to act as a medical AI and return top 3 conditions
A user message containing the symptoms
3. Prompt formatting (line 16)

apply_chat_template converts the message list into the model's native chat format (e.g. <|system|>...<|user|>...)
4. Generation (lines 17–18)

GenerationConfig controls output: up to 200 new tokens, with sampling at low temperature (0.2) for focused/deterministic responses
The pipeline runs inference and returns the generated text
5. Output (line 19)

Prints the full generated text, including the original prompt + model response
In summary: it's a single-file proof-of-concept that uses a gated-free open LLM locally to simulate a simple clinical decision support tool — no API calls, no fine-tuning, pure zero-shot prompting.
#--- SDML0.py ------------------------------------
(venv) user@user:/media/user/dsk64/monowork$ python SDML0.py
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 218/218 [00:00<00:00, 2751.65it/s]
[transformers] Ignoring clean_up_tokenization_spaces=True for BPE tokenizer GPT2Tokenizer. The clean_up_tokenization post-processing step is designed for WordPiece tokenizers and is destructive for BPE (it strips spaces before punctuation). Set clean_up_tokenization_spaces=False to suppress this warning, or set clean_up_tokenization_spaces_for_bpe_even_though_it_will_corrupt_output=True to force cleanup anyway.

---------------------------------------------------------
--- Demo Mode: Fallback Response ---
<|im_start|>system
You are a medical AI assistant. Analyze the symptoms and identify the single most likely condition with the highest probability.<|im_end|>
<|im_start|>user
I have a high fever, dry cough, and severe fatigue.<|im_end|>
<|im_start|>assistant
Based on the symptoms you've provided, the most likely condition is: 

Influenza, also known as the flu. This is because a high fever, dry cough, and severe fatigue are all common symptoms of the flu.
#=== SDML0.go ============================================
--- Demo Mode: Fallback Response ---
<|im_start|>system
You are a medical AI assistant. Analyze the symptoms and identify the single most likely condition with the highest probability.
<|im_end|>
<|im_start|>user
I have a high fever, dry cough, and severe fatigue.
<|im_end|>
<|im_start|>assistant
Based on the symptoms you've provided, the most likely condition is:

Influenza (Flu): This is a viral infection that causes symptoms like fever, cough, and fatigue. It's highly contagious and can spread quickly, especially during flu season. 
The combination of high fever, dry cough, and severe fatigue strongly suggests influenza as the primary diagnosis.

Please remember that this is just a potential condition and it's important to consult with a healthcare professional for a proper diagnosis.

#=== SDML1 ===============================================
Completed successfully. SmolLM2-1.7B-Instruct was downloaded (~3.4GB) and produced solid travel recommendations:

Santorini, Greece — history (Akrotiri), beaches, hiking trails around Oia
Cinque Terre, Italy — 5 coastal towns, scenic hiking trails, local seafood
Porto, Portugal — riverfront, history... (cut off at max_new_tokens=200)
The output was truncated mid-sentence on Porto. Want me to increase max_new_tokens to get the full response?


