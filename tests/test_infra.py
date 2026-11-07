import os
import subprocess
import pytest

def run_docker_command(cmd):
    container_name = os.getenv("CONTAINER_NAME", "python_app_service")
    full_cmd = f"docker exec {container_name} {cmd}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result

def test_container_user_is_not_root():
    res = run_docker_command("whoami")
    assert res.returncode == 0
    username = res.stdout.strip()
    assert username != "root"
    assert username == "appuser"


def test_gunicorn_process_running():
    check_script = "import os; print([x for x in os.listdir('/proc') if x.isdigit() and 'gunicorn' in open(f'/proc/{x}/cmdline', 'r', errors='ignore').read()])"
    res = run_docker_command(f"python -c \"{check_script}\"")

    assert res.returncode == 0
    assert res.stdout.strip() != "[]"

def test_port_listening():
    res = run_docker_command("python -c \"import socket; s = socket.socket(); s.connect(('127.0.0.1', 5000)); print('OK')\"")
    assert res.returncode == 0
    assert "OK" in res.stdout