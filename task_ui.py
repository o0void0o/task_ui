
# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "http://10.0.0.138:8002"

@app.route('/')
def index():
    # Fetch only open tasks from the API
    response = requests.get(f"{API_BASE_URL}/tasks", params={"status": "open"})
    tasks = response.json() if response.status_code == 200 else []
    
    return render_template('index.html', tasks=tasks)

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    # Update the task status to 'completed'
    response = requests.put(f"{API_BASE_URL}/tasks/{task_id}", json={"status": "completed"})
    
    if response.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if not title:
        return jsonify({"success": False, "error": "Title is required"}), 400

    # Create a new task
    response = requests.post(f"{API_BASE_URL}/tasks", json={"title": title})
    
    if response.status_code == 201:
        new_task = response.json()
        return jsonify({"success": True, "task": new_task})
    else:
        return jsonify({"success": False, "error": "Failed to create task"}), 400


if __name__ == '__main__':
 app.run(host="0.0.0.0", port=8003, debug=True)