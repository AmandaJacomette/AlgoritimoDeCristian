import socket
import time
from datetime import datetime, timedelta

# Configurações de IP e porta do servidor
SERVER_IP = "192.168.1.10"
PORT = 12345

class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.local_time = datetime.now()

    def request_time(self):
        t0 = time.time()
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, PORT))
            server_time = client_socket.recv(1024).decode()
            t1 = time.time()

            network_delay = (t1 - t0) / 2
            adjusted_time = datetime.fromisoformat(server_time) + timedelta(seconds=network_delay)
            self.gradual_adjustment(adjusted_time)
        except Exception as e:
            print(f"Erro na sincronização de {self.name}: {e}")

    def gradual_adjustment(self, target_time):
        diff = (target_time - self.local_time).total_seconds()
        adjustment_steps = 10
        step_value = diff / adjustment_steps

        for _ in range(adjustment_steps):
            self.local_time += timedelta(seconds=step_value)
            time.sleep(0.5)
        print(f"{self.name} sincronizado para {self.local_time.strftime('%H:%M:%S')}")

def periodic_sync(device, interval=5):
    while True:
        device.request_time()
        time.sleep(interval)

# Inicialização do Cliente
if __name__ == "__main__":
    device = Device("Device", "192.168.1.11")  # Mude o IP para o da máquina correta
    periodic_sync(device)
