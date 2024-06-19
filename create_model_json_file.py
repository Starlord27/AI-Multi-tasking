from transformers import AutoTokenizer, AutoModelForCausalLM
import os

model_name = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
model_path = "M:/Model IA/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"

# Assurez-vous que le répertoire existe
os.makedirs(model_path, exist_ok=True)

# Télécharger et sauvegarder les fichiers nécessaires
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_path)
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=model_path)

# Sauvegarder les fichiers localement
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print(f"Modèle et tokenizer sauvegardés dans {model_path}")
