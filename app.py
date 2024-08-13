import os
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

# Получаем названия контейнеров из переменных окружения
container1 = os.getenv('CONTAINER1')
container2 = os.getenv('CONTAINER2')

# Логирование названий контейнеров
app.logger.info(f"Container 1: {container1}")
app.logger.info(f"Container 2: {container2}")

# Функция для генерации токена
def generate_token():
    app.logger.info("Generating token...")
    result = subprocess.run(
        ["docker", "exec", "gov-portal-db", "./airdao-gov-portal-db", "gen-token", "-l", "86400"],
        stdout=subprocess.PIPE
    )
    token = result.stdout.decode('utf-8').strip()
    app.logger.info(f"Generated token: {token}")
    return token

# Функция для проверки статуса контейнера
def check_container_status(container_name):
    app.logger.info(f"Checking status of container: {container_name}")
    result = subprocess.run(
        ["docker", "inspect", "--format='{{.State.Running}}'", container_name],
        stdout=subprocess.PIPE
    )
    status = result.stdout.decode('utf-8').strip()
    app.logger.info(f"Status of container {container_name}: {status}")
    return status == "'true'"

# Эндпоинты для проверки статуса контейнеров
@app.route('/check-status/container1', methods=['GET'])
def check_status_container1():
    if container1 is None:
        app.logger.error("CONTAINER1 environment variable is not set")
        return jsonify({"error": "CONTAINER1 not set"}), 400
    is_running = check_container_status(container1)
    if is_running:
        return jsonify({"status": "running", "container": container1}), 200
    else:
        return jsonify({"status": "stopped", "container": container1}), 404

@app.route('/check-status/container2', methods=['GET'])
def check_status_container2():
    if container2 is None:
        app.logger.error("CONTAINER2 environment variable is not set")
        return jsonify({"error": "CONTAINER2 not set"}), 400
    is_running = check_container_status(container2)
    if is_running:
        return jsonify({"status": "running", "container": container2}), 200
    else:
        return jsonify({"status": "stopped", "container": container2}), 404

@app.route('/check-status/<container_name>', methods=['GET'])
def check_status(container_name):
    app.logger.info(f"Received request for status of container: {container_name}")
    is_running = check_container_status(container_name)
    if is_running:
        return jsonify({"status": "running", "container": container_name}), 200
    else:
        return jsonify({"status": "stopped", "container": container_name}), 404

if __name__ == '__main__':
    app.logger.info("Starting check-status application...")
    app.run(host='0.0.0.0', port=5017)
