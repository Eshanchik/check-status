import os
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

# Получаем названия контейнеров из переменных окружения
container1 = os.getenv('CONTAINER1')
container2 = os.getenv('CONTAINER2')

# Функция для генерации токена
def generate_token():
    result = subprocess.run(
        ["docker", "exec", "gov-portal-db", "./airdao-gov-portal-db", "gen-token", "-l", "86400"],
        stdout=subprocess.PIPE
    )
    token = result.stdout.decode('utf-8').strip()
    return token

# Функция для проверки статуса контейнера
def check_container_status(container_name):
    result = subprocess.run(
        ["docker", "inspect", "--format='{{.State.Running}}'", container_name],
        stdout=subprocess.PIPE
    )
    status = result.stdout.decode('utf-8').strip()
    return status == "'true'"

# Эндпоинты для проверки статуса контейнеров
@app.route('/check-status/container1', methods=['GET'])
def check_status_container1():
    is_running = check_container_status(container1)
    if is_running:
        return jsonify({"status": "running", "container": container1}), 200
    else:
        return jsonify({"status": "stopped", "container": container1}), 404

@app.route('/check-status/container2', methods=['GET'])
def check_status_container2():
    is_running = check_container_status(container2)
    if is_running:
        return jsonify({"status": "running", "container": container2}), 200
    else:
        return jsonify({"status": "stopped", "container": container2}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5017)
