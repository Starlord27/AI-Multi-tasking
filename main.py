from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import hashlib
import queue
import logging
from llama_cpp import Llama
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app)

# Charger le modèle sur le serveur
model_path = "M:/Model IA/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf"
model = Llama(model_path=model_path)
logging.debug(f"Model loaded from {model_path}")

task_queue = queue.Queue()
results = {}
task_in_progress = None

@app.route('/v1/models', methods=['GET'])
def get_models():
    return jsonify({"models": ["Mistral-7B-Instruct-v0.2"]})

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    global task_in_progress
    try:
        data = request.json
        prompt = data.get('prompt', '')
        logging.debug(f"Received prompt: {prompt}")

        task_id = hashlib.md5(prompt.encode()).hexdigest()
        logging.debug(f"Generated task ID: {task_id}")

        task = {
            "task_id": task_id,
            "prompt": prompt
        }
        task_queue.put(task)
        logging.debug(f"Task put in queue: {task}")

        # Notify clients about the new task only if no task is in progress
        if task_in_progress is None:
            socketio.emit('new_task_available')
            logging.debug("Emitted new_task_available event")

        while task_id not in results:
            socketio.sleep(0.1)

        response_text = results.pop(task_id)
        logging.debug(f"Response received: {response_text}")
        response_json = {"response": response_text}
        logging.debug(f"Sending response: {response_json}")
        return jsonify(response_json)
    except Exception as e:
        logging.error("Error in chat_completions", exc_info=e)
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    logging.debug('Client connected')
    emit('ready_for_task')

@socketio.on('disconnect')
def handle_disconnect():
    global task_in_progress
    logging.debug('Client disconnected')
    task_in_progress = None

@socketio.on('ready_for_task')
def handle_ready_for_task():
    global task_in_progress
    logging.debug('Client ready for task')
    if not task_queue.empty() and task_in_progress is None:
        task = task_queue.get()
        task_in_progress = task["task_id"]
        logging.debug(f"Sending task to client: {task}")
        emit('task', task)
    else:
        logging.debug("No tasks in queue or task already in progress")

@socketio.on('task_result')
def handle_task_result(data):
    global task_in_progress
    logging.debug(f"Received task result from client: {data}")
    task_id = data['task_id']
    result = data['result']
    results[task_id] = result
    task_in_progress = None
    socketio.emit('new_task_available')  # Notify clients about the new task
    logging.debug('Emitted new_task_available after task result')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
