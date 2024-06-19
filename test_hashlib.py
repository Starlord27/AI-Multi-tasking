import hashlib

def test_hashlib():
    prompt = "Your test prompt here"
    task_id = hashlib.md5(prompt.encode()).hexdigest()
    print(f"Task ID: {task_id}")

if __name__ == '__main__':
    test_hashlib()
