import bluetooth # type: ignore
import json

from ..config.wifi_config import WiFiConfig
from ..config.test_handler import TestHandler
from ..config.cable_config import CableConfig
from ..config.status_handler import StatusHandler
from ..config.maintenance_handler import MaintenanceHandler
from ..config.integracoes_handler import IntegracaoHandler

def handle_config(dados, client_sock):
    '''
    Function to handle configuration received 
    Função para lidar com a configuração recebida via Bluetooth.

    Parâmetros:
    dados (dict): Dicionário contendo os dados de configuração.
    client_sock: Socket do cliente Bluetooth.
    '''
    tipo = dados.get("type", "").lower()

    print(f"[BluetoothServer]: Tipo recebido: {tipo}")

    if tipo == "wi-fi":
        WiFiConfig(
            ssid=dados.get("ssid", ""),
            pwd=dados.get("password", ""),
            ip=dados.get("ip", ""),
            msk=dados.get("mask", ""),
            gw=dados.get("gateway", "")
        ).apply()

    elif tipo == "cable":
        CableConfig(
            ip=dados.get("ip", ""),
            msk=dados.get("mask", ""),
            gw=dados.get("gateway", "")
        ).apply()

    elif tipo == "status":
        StatusHandler().handle(client_sock)

    elif tipo == "teste":
        TestHandler(dados.get("ip", "")).handle()

    elif tipo == "manutencao":
        MaintenanceHandler().handle()
    
    elif tipo == "integr":
        IntegracaoHandler.handler(client_sock)

    else:
        print(f"[BluetoothServer]: Tipo '{tipo}' não reconhecido.")


def iniciar_servidor():
    '''
    Inicia o servidor Bluetooth para receber configurações.

    Configuracoes:
        - Canal RFCOMM: 1
    '''
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)

    print(f"[BluetoothServer]: Aguardando conexões no canal {port}...")

    try:
        while True:
            client_sock, client_info = server_sock.accept()
            print(f"[BluetoothServer]: Conectado a {client_info}")

            try:
                while True:
                    data = client_sock.recv(1024)
                    if not data:
                        break

                    msg = data.decode().strip()
                    if msg.lower() == "by":
                        break

                    try:
                        dados = json.loads(msg)
                        handle_config(dados, client_sock)

                    except json.JSONDecodeError:
                        print("[BluetoothServer]: Erro ao decodificar JSON")

            finally:
                client_sock.close()

    finally:
        server_sock.close()
