import time
import socket
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

HTTP_PORT = 9050
HTTP_ENDPOINT = '/dateTimeNow'
COOLDOWN_TIME = 30

class TcpClient:
    '''
    Classe responsável por realizar requisições HTTP para obter a data e hora atual de um servidor remoto.
    Methods
    
    '''
    
    def get_datetime_now(self, host, port=HTTP_PORT):
        '''
        Realiza uma requisição HTTP para obter a data e hora atual do servidor especificado.
        Parâmetros:
            - host (str): Endereço IP ou hostname do servidor.
            - port (int): Porta do servidor HTTP (padrão: 9050).
        '''
        url = f'http://{host}:{port}{HTTP_ENDPOINT}'

        hostname = subprocess.run(["hostname"], capture_output=True, text=True)

        try:
            req = Request(url, headers={"User-Agent": hostname.stdout.strip()})
            with urlopen(req, timeout=COOLDOWN_TIME) as response:
                body = response.read().decode('utf-8', errors='replace')
                print(f"[TcpClient] {url} -> {response.status} | {body[:200]}")
                self.define_datetime(body[:200].strip())
        except HTTPError as e:
            print(f"[HTTP] {url} -> HTTP {e.code}")
        except URLError as e:
            print(f"[HTTP] {url} -> erro de rede: {e.reason}")
        except Exception as e:
            print(f"[HTTP] {url} -> falha: {e}")
    
    def define_datetime(self, datetime_str):
        '''
        Define a data e hora do sistema com base na string fornecida.

        Parâmetros:
            - datetime_str (str): String representando a data e hora no formato 'YYYY-MM-DD HH:MM:SS'.
        '''
        try:
            subprocess.run(['sudo', 'timedatectl', 'set-time', datetime_str], check=True)
            print(f"[TcpClient] Data e hora definidas para: {datetime_str}")
        except subprocess.CalledProcessError as e:
            print(f"[TcpClient] Erro ao definir data e hora: {e}")