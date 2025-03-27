import socket
import time
import os
from datetime import datetime, timedelta

# Configurações de IP e porta do servidor
IP_SERVIDOR = "192.168.1.10"
PORTA = 12345

class Dispositivo:
    """Classe que representa um dispositivo cliente que sincroniza seu relógio com o servidor gradualmente."""
    
    def __init__(self, nome, ip, ajuste_por_ciclo=0.1):
        self.nome = nome
        self.ip = ip
        self.ajuste_por_ciclo = ajuste_por_ciclo  # Ajuste progressivo em segundos

    def solicitar_horario(self):
        """
        Solicita o horário ao servidor, calcula o atraso de rede e ajusta o horário local gradualmente.
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

            # Obtém o horário atual do sistema
            hora_atual = datetime.now()

            # Calcula a diferença entre os horários
            diferenca = (hora_ajustada - hora_atual).total_seconds()

            # Ajuste gradual
            self.ajustar_horario_gradualmente(diferenca)
        except Exception as erro:
            print(f"Erro na sincronização de {self.nome}: {erro}")

    def ajustar_horario_gradualmente(self, diferenca):
        """
        Ajusta o horário do sistema operacional de forma gradual.
        """
        if abs(diferenca) < 0.1:
            print(f"{self.nome}: Ajuste desnecessário, diferença pequena ({diferenca:.6f}s)")
            return

        print(f"{self.nome}: Diferença de {diferenca:.6f}s detectada, ajustando gradualmente...")

        incremento = self.ajuste_por_ciclo if diferenca > 0 else -self.ajuste_por_ciclo

        while abs(diferenca) > self.ajuste_por_ciclo:
            hora_atual = datetime.now() + timedelta(seconds=incremento)
            novo_horario = hora_atual.strftime('%H:%M:%S')
            nova_data = hora_atual.strftime('%Y-%m-%d')

            os.system(f"sudo date -s '{nova_data} {novo_horario}'")

            diferenca -= incremento
            time.sleep(1)  # Pequeno atraso para ajuste progressivo

        print(f"{self.nome}: Sincronização concluída.")

def sincronizacao_periodica(dispositivo, intervalo=5):
    """
    Mantém a sincronização do dispositivo em intervalos regulares.
    """
    while True:
        dispositivo.solicitar_horario()
        time.sleep(intervalo)

# Inicialização do Cliente
if __name__ == "__main__":
    dispositivo = Dispositivo("Dispositivo", "192.168.1.11", ajuste_por_ciclo=0.1)
    sincronizacao_periodica(dispositivo)
