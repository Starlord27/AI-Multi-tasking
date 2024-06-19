from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import queue

app = Flask(__name__)
socketio = SocketIO(app)

model_name = "gpt2"  # Exemple de modèle
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Définir les GPUs disponibles
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Queue pour les tâches
task_queue = queue.Queue()

# Dictionnaire pour stocker les résultats des tâches
results = {}


@app.route('/v1/models', methods=['GET'])
def get_models():
    return jsonify({"models": [model_name]})


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    prompt = data.get('prompt', '')
    task_id = hashlib.md5(prompt.encode()).hexdigest()
    task = {
        "task_id": task_id,
        "task": "chat_completions",
        "prompt": prompt
    }
    task_queue.put(task)

    # Attendre que la tâche soit complétée
    while task_id not in results:
        socketio.sleep(0.1)

    response = results.pop(task_id)
    return jsonify(response)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('ready_for_task')
def handle_ready_for_task():
    if not task_queue.empty():
        task = task_queue.get()
        emit('task', task)


@socketio.on('task_result')
def handle_task_result(data):
    task_id = data['task_id']
    results[task_id] = data['result']
    emit('ready_for_task')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
