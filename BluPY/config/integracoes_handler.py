import json
from typing import Dict, Any, List

class IntegracaoHandler:
    '''
    Classe para lidar com as integrações do sistema.
    '''
    @staticmethod
    def loadAll(path: str = "/usr/bin/integracoes_Config.json") -> Dict[str, Any]:
        '''
        Carrega todas as integrações do arquivo de configuração.
        '''
        with open(path, "r") as f:
            data = json.load(f)

        integracoes = data.get("integracoes", {}) if isinstance(data, dict) else {}

        estado = {
            nome: (dados or {}).get("isAtivo", False)
            for nome, dados in integracoes.items()
        }

        ativas = {
            nome: dados
            for nome, dados in integracoes.items()
            if (dados or {}).get("isAtivo", False)
        }

        nomes_ativas = [nome for nome, ativo in estado.items() if ativo]

        return {
            "estado": estado,
            "ativas": ativas,
            "nomes_ativas": nomes_ativas
        }
    
    def handler(client_sock) -> List[str]:
        '''
        Envia as integrações via Bluetooth.
        '''
        try:
            integracoes = IntegracaoHandler.loadAll()
        
            resposta = {
                    "integracoes": integracoes
                }

            client_sock.send((json.dumps(resposta) + "\n").encode())
            print(f"[IntegracoesHandler]: Resposta enviada: {resposta}")
            print("[IntegracoesHandler]: Status enviado com sucesso.")

        except Exception as e:
            err = {"error": f"integracoes: {e}"}
            client_sock.send((json.dumps(err) + "\n").encode())
            print(f"[IntegracoesHandler]: Erro ao processar status: {e}")
