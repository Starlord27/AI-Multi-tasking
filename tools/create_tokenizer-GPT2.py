from transformers import GPT2Tokenizer, GPT2Model
import os

model_name = "gpt2"  # Utiliser un tokenizer GPT-2 standard
model_path = "M:/Model IA/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"

# Assurez-vous que le répertoire existe
os.makedirs(model_path, exist_ok=True)

# Télécharger et sauvegarder le tokenizer nécessaire
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(model_path)

print(f"Tokenizer sauvegardé dans {model_path}")
