import socket
from ..services.tcp_client import TcpClient

class UdpListenerConfig:
    '''
    Classe para ouvir broadcasts UDP e interagir com TcpClient.
    '''
    def __init__(self):
        self.tcp = TcpClient()

    def listen_for_broadcasts(self,port=9050, bufsize=1024):
        '''
        Ouve broadcasts UDP na porta especificada.
        
        Parâmetros:
            - port (int): Porta para ouvir broadcasts UDP.
            - bufsize (int): Tamanho do buffer para receber mensagens.
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            print("Listening for broadcasts on port 9050...")
        except socket.error as e:
            print(f"Socket error: {e}")
            pass
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        sock.bind(('', port))
        print(f"[UDP] Ouvindo broadcast em {port}")
        
        try:
            while True:
                data, addr = sock.recvfrom(bufsize)

                try: 
                    msg =data.decode(errors='replace').strip()
                except Exception as e:
                    msg = str(data)

                ip = msg or addr[0]

                print(f"[UDP] Mensagem: {msg}")
                
                self.tcp.get_datetime_now(ip)

        except KeyboardInterrupt:
            print(f"[UDP] Encerrando listener")

        finally:
            sock.close()
            print("[UDP] Socket fechado.")