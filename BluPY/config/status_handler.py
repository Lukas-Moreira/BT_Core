import json
import os
from .base_config import BaseConfig

class StatusHandler:
    '''
    Class to handle the status of the collector. It reads the ping results and collector configuration,
    and sends information via Bluetooth.

    Parameters:
        - client_sock: Bluetooth client socket.
    '''
    version = "v2.0.0"

    def handle(self, client_sock):
        '''
        Sends the status of the collector via Bluetooth.

        Parameters:
            - client_sock: Bluetooth client socket.
        '''
        print("[StatusHandler]: Sending collector status...")

        try:
            with open("ping_result.json", "r") as f1:
                ping = json.load(f1)

            with open("/home/rock/Logs/coletor_data.json", "r") as f2:
                config = json.load(f2)

            ip = BaseConfig.get_first_active_ip()

            resposta = {
                "version": self.version,
                "ip": ip or "No IP address",
                "success": "true" if ping.get("success") else "false",
                "packet_loss": f"{min(100, max(0, float(ping.get('packet_loss_percent', 0)))):.2f}%",
                "rtt_avg": f"{ping.get('rtt_avg_ms', 0)/100:.2f} ms",
                "timestamp": ping.get("timestamp", ""),
                "responses_ms": ping.get("responses_ms",[]),
                "tipo_coletor": config.get("status", {}).get("tipo_coletor", "unknown"), 
                "versao_codigo": config.get("status", {}).get("versao_codigo", "unknown"),
                "config": config.get("config", []),
            }

            client_sock.send((json.dumps(resposta) + "\n").encode())
            print(f"[StatusHandler]: Response sent: {resposta}")
            print("[StatusHandler]: Status sent successfully.")

        except Exception as e:
            print(f"[StatusHandler]: Error processing status: {e}")