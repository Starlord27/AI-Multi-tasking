from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import shutil

# Utiliser un modèle GPT-2 pour le test
model_name = "gpt2"
model_path = "M:/Model IA/gpt2"

# Supprimez le répertoire existant s'il existe pour éviter les conflits
if os.path.exists(model_path):
    shutil.rmtree(model_path)

# Assurez-vous que le répertoire existe
os.makedirs(model_path, exist_ok=True)

# Télécharger et sauvegarder les fichiers nécessaires
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_path)
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=model_path)

# Sauvegarder les fichiers localement
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)

print(f"Modèle et tokenizer sauvegardés dans {model_path}")
