import socket
import time
import os
from datetime import datetime, timedelta

# Configurações de IP e porta do servidor
IP_SERVIDOR = "192.168.1.10"
PORTA = 12345

class Dispositivo:
    """Classe que representa um dispositivo cliente que sincroniza seu relógio com o servidor."""
    
    def __init__(self, nome, ip):
        self.nome = nome
        self.ip = ip

    def solicitar_horario(self):
        """
        Solicita o horário ao servidor, calcula o atraso de rede e ajusta o horário local.
        """
        t0 = time.time()  # Marca o tempo antes da solicitação
        try:
            # Criação do socket para comunicação com o servidor
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_cliente.connect((IP_SERVIDOR, PORTA))

            # Recebe o horário do servidor
            hora_servidor = socket_cliente.recv(1024).decode()
            t1 = time.time()  # Marca o tempo após a resposta

            # Calcula o atraso da rede (round-trip time / 2)
            atraso_rede = (t1 - t0) / 2
            hora_ajustada = datetime.fromisoformat(hora_servidor) + timedelta(seconds=atraso_rede)

            # Ajusta o horário do dispositivo
            self.ajustar_horario(hora_ajustada)
        except Exception as erro:
            print(f"Erro na sincronização de {self.nome}: {erro}")

    def ajustar_horario(self, hora_alvo):
        """
        Ajusta o horário do sistema operacional para o horário calculado.
        """
        novo_horario = hora_alvo.strftime('%H:%M:%S')
        novo_data = hora_alvo.strftime('%Y-%m-%d')

        os.system(f"sudo date -s '{novo_data} {novo_horario}'")

        print(f"{self.nome} sincronizado para {novo_horario}")

def sincronizacao_periodica(dispositivo, intervalo=5):
    """
    Mantém a sincronização do dispositivo em intervalos regulares.
    """
    while True:
        dispositivo.solicitar_horario()
        time.sleep(intervalo)

# Inicialização do Cliente
if __name__ == "__main__":
    dispositivo = Dispositivo("Dispositivo", "192.168.1.11")  # Ajuste o IP conforme necessário
    sincronizacao_periodica(dispositivo)
