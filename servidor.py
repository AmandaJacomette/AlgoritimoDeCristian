import socket
import threading
import time
import os
from datetime import datetime
import ntplib  # Biblioteca para conexão com servidores NTP

# Configurações de IP e porta
IP_SERVIDOR = "192.168.1.10"
PORTA = 12345

class ServidorHorario:
    """Classe que representa um servidor de tempo baseado no protocolo NTP."""
    
    def __init__(self):
        # Configuração do socket do servidor
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((IP_SERVIDOR, PORTA))
        self.servidor.listen(5)  # Aceita até 5 conexões simultâneas

        # Inicia a atualização do horário do servidor em uma thread separada
        threading.Thread(target=self.atualizar_horario, daemon=True).start()
        print(f"Servidor NTP ativo em {IP_SERVIDOR}:{PORTA}")

    def atualizar_horario(self):
        """
        Obtém o horário atualizado de um servidor NTP e ajusta o horário do sistema.
        """
        cliente_ntp = ntplib.NTPClient()
        while True:
            try:
                # Solicita o horário a um servidor NTP público
                resposta = cliente_ntp.request('pool.ntp.org', version=3)
                hora_ntp = datetime.fromtimestamp(resposta.tx_time)

                # Atualiza o relógio do sistema com o horário obtido
                self.definir_horario_sistema(hora_ntp)
            except Exception as erro:
                print(f"Erro ao atualizar via NTP: {erro}")
            
            # Atualiza a cada 60 segundos
            time.sleep(60)

    def definir_horario_sistema(self, hora_alvo):
        """
        Altera o horário do sistema operacional para o horário obtido do servidor NTP.
        """
        novo_horario = hora_alvo.strftime('%H:%M:%S')
        novo_data = hora_alvo.strftime('%Y-%m-%d')

        os.system(f"sudo date -s '{novo_data} {novo_horario}'")

        print(f"Hora do servidor atualizada via NTP para {hora_alvo}")

    def iniciar(self):
        """
        Aguarda conexões de clientes e fornece o horário atual do servidor.
        """
        while True:
            socket_cliente, endereco = self.servidor.accept()
            print(f"Conexão recebida de {endereco}")

            # Envia a hora atual do servidor para o cliente
            hora_atual = str(datetime.now())
            socket_cliente.send(hora_atual.encode())

            # Fecha a conexão com o cliente
            socket_cliente.close()

# Inicialização do Servidor
if __name__ == "__main__":
    servidor = ServidorHorario()
    servidor.iniciar()
