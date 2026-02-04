import subprocess, time, re, json, os

class TestHandler:
    '''
    Classe para realizar testes de conectividade via ping.

    Parâmetros:
        - ip (str): Endereço IP ou hostname para o teste de ping.
    '''
    def __init__(self, ip):
        self.ip = ip

    def handle(self):
        '''
        Envia o status do coletor via Bluetooth.

        Parâmetros:
            - client_sock: Socket do cliente Bluetooth.
        '''
        print("[TestHandler]: Iniciando teste de ping...")

        try:
            subprocess.run(["sudo", "rm", "ping_result.json"], check=False)

            result = subprocess.run(["ping", "-c", "51", "-i", "0.5", "-W", "0.5", self.ip],
                                    capture_output=True, text=True)

            output = result.stdout

            response_times = [float(m.group(1)) for m in re.finditer(r'time=([\d.]+) ms', output)]
            packet_loss = re.search(r"([\d.]+)% packet loss", output)
            rtt = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)", output)

            ping_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ip": self.ip,
                "success": result.returncode == 0,
                "packet_loss_percent": round(float(packet_loss.group(1)), 2) if packet_loss else 100.0,
                "rtt_avg_ms": float(rtt.group(1)) if rtt else 0.0,
                "responses_ms": response_times
            }

            with open("ping_result.json", "w") as f:
                json.dump(ping_data, f, indent=4)

            print("[TestHandler]: Resultado salvo com sucesso.")

        except Exception as e:
            print(f"[TestHandler]: Erro: {e}")
