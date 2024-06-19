import socketio
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

sio = socketio.Client()

server_url = "http://192.168.1.20:5000"

@sio.event
def connect():
    logging.debug('Connection established')
    sio.emit('ready_for_task')
    logging.debug('Emitted ready_for_task')

@sio.event
def disconnect():
    logging.debug('Disconnected from server')

@sio.on('task')
def on_task(data):
    logging.debug(f'Received task: {data}')
    task_id = data["task_id"]
    prompt = data["prompt"]

    try:
        logging.debug(f'Sending prompt to server model: {prompt}')
        response = requests.post(f"{server_url}/v1/chat/completions", json={"prompt": prompt}, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        response_text = response_data.get("response", "Error: No response from model")
        logging.debug(f'Received response from server model: {response_text}')

        result = {
            "task_id": task_id,
            "result": response_text
        }
        logging.debug(f'Sending task result: {result}')
        sio.emit('task_result', result)
        logging.debug('Emitted task_result')

    except requests.exceptions.RequestException as e:
        logging.error(f'Error processing task: {e}')
        result = {
            "task_id": task_id,
            "result": f"Error: {e}"
        }
        sio.emit('task_result', result)
        logging.debug('Emitted task_result with error')

    sio.emit('ready_for_task')
    logging.debug('Emitted ready_for_task')

@sio.on('new_task_available')
def on_new_task_available():
    logging.debug('New task available, emitting ready_for_task')
    sio.emit('ready_for_task')

if __name__ == '__main__':
    sio.connect(server_url)
    sio.wait()
