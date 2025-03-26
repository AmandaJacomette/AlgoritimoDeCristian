import socket
import threading
import time
from datetime import datetime
import ntplib  # Biblioteca para conexão com NTP

# Configurações de IP e porta
SERVER_IP = "192.168.1.10"
PORT = 12345

class TimeServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER_IP, PORT))
        self.server.listen(5)
        self.current_time = datetime.now()  # Hora inicial
        threading.Thread(target=self.update_time, daemon=True).start()  # Atualização periódica
        print(f"Servidor NTP ativo em {SERVER_IP}:{PORT}")

    def update_time(self):
        ntp_client = ntplib.NTPClient()
        while True:
            try:
                response = ntp_client.request('pool.ntp.org', version=3)
                self.current_time = datetime.fromtimestamp(response.tx_time)
                print(f"Hora do servidor atualizada via NTP: {self.current_time}")
            except Exception as e:
                print(f"Erro ao atualizar via NTP: {e}")
            time.sleep(60)  # Atualiza a cada 60 segundos

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f"Conexão recebida de {addr}")
            current_time = str(datetime.now())
            client_socket.send(current_time.encode())
            client_socket.close()

# Inicialização do Servidor
if __name__ == "__main__":
    server = TimeServer()
    server.start()
