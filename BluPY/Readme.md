# 🔧 Coletor de Configuração via Bluetooth SPP
# Setup_ConnectionsPy

Projeto para configuração e manutenção de conectividade de coletores via Bluetooth e listeners de rede.

**Resumo:**
- Fornece um servidor Bluetooth (RFCOMM) que recebe comandos JSON para aplicar configurações de rede (Wi‑Fi e cabeada), retornar status, executar testes de conectividade e listar integrações.
- Inclui um listener UDP que recebe broadcasts (porta 9050) e aciona requisições HTTP para sincronizar data/hora do sistema.

**Principais componentes**
- `application/main.py`: ponto de entrada. Inicia `UdpListenerConfig` (listener UDP na porta 9050) e o servidor Bluetooth.
- `services/bluetooth_server.py`: servidor RFCOMM que aceita JSONs e dispara handlers conforme o campo `type`.
- `services/udp_listener.py`: escuta broadcasts UDP e delega a `services/tcp_client.py` para obter data/hora remota.
- `services/tcp_client.py`: realiza requisição HTTP ao endpoint `/dateTimeNow` do host indicado e tenta ajustar o relógio do sistema via `timedatectl`.
- `config/`:
  - `wifi_config.py`: aplica configurações Wi‑Fi usando `nmcli`.
  - `cable_config.py`: aplica configuração de rede cabeada usando `nmcli`.
  - `base_config.py`: utilitários (conversão de máscara para CIDR, obtenção do IP ativo).
  - `test_handler.py`: executa testes de ping e grava `ping_result.json`.
  - `status_handler.py`: compõe e envia um resumo de status (lê `ping_result.json` e `/home/rock/Logs/coletor_data.json`).
  - `maintenance_handler.py`: placeholder para ativar modo de manutenção.
  - `integracoes_handler.py`: carrega `integracoes_Config.json` (por padrão `/usr/bin/integracoes_Config.json`) e envia integrações via Bluetooth.

**Fluxos/Comandos Bluetooth**
Enviar JSONs via conexão RFCOMM (canal 1). Exemplos de payloads:

- Wi‑Fi:
```
{ "type": "wi-fi", "ssid": "MINHA_REDE", "password": "senha", "ip": "192.168.1.100", "mask": "255.255.255.0", "gateway": "192.168.1.1" }
```
- Rede cabeada:
```
{ "type": "cable", "ip": "192.168.1.50", "mask": "255.255.255.0", "gateway": "192.168.1.1" }
```
- Status do coletor:
```
{ "type": "status" }
```
- Teste de ping:
```
{ "type": "teste", "ip": "8.8.8.8" }
```
- Integrações:
```
{ "type": "integr" }
```

**Listener UDP**
- Porta: `9050` (padrão).
- Ao receber um broadcast, o listener tenta extrair um IP da mensagem e chama `TcpClient.get_datetime_now(ip)` para sincronizar horário.

**Requisitos**
- Sistema operacional: Linux (scripts usam `sudo`, `nmcli`, `timedatectl` e `ping`). Não testado no Windows.
- Python 3.x
- Dependências Python (ex.:): `netifaces`, `pybluez` (ou outra lib Bluetooth compatível). Instale via `pip install netifaces pybluez`.

**Instalação e execução**
1. Certifique-se de ter `nmcli`, `timedatectl` e permissões sudo.
2. Instale dependências Python: `pip install -r requirements.txt` ou `pip install netifaces pybluez`.
3. Execute o aplicativo:
```
python application/main.py
```

**Arquivos e caminhos importantes**
- `ping_result.json`: criado por `TestHandler` (no CWD).
- `/home/rock/Logs/coletor_data.json`: arquivo lido por `StatusHandler` — ajuste conforme sua instalação.
- `integracoes_Config.json`: por padrão em `/usr/bin/integracoes_Config.json` (alterar se necessário).

**Observações**
- Muitos comandos usam `sudo` e utilitários de rede do Linux; execute em ambiente com privilégios adequados.
- O servidor Bluetooth espera conexões RFCOMM no canal 1.
- Os handlers assumem que arquivos de configuração e logs existem na máquina; adapte caminhos conforme o ambiente.

Se desejar, posso:
- adicionar um `requirements.txt` com as dependências detectadas,
- criar exemplos de scripts para testar o servidor Bluetooth,
- ou ajustar caminhos padrão (ex.: `coletor_data.json`) para torná-los configuráveis.

Este projeto permite configurar automaticamente a rede (Wi-Fi ou cabeada) de um dispositivo **Rock Pi S** ou similar via conexão **Bluetooth Serial Port Profile (SPP)**. A comunicação é feita por socket RFCOMM, com troca de mensagens em JSON.

---

## 📦 Geração do Executável

Para compilar a aplicação Python em um executável único, utilize o `PyInstaller`:

```bash
pyinstaller --onefile setup.py
```

O executável será gerado em `./dist/setup`.

---

## 🚀 Funcionalidades

- Recebe comandos via Bluetooth SPP no formato JSON.
- Aplica configuração de rede **Wi-Fi** ou **cabo Ethernet** via `nmcli`.
- Suporte a:
  - `type: "wi-fi"`: conecta a uma rede Wi-Fi com IP estático.
  - `type: "cable"`: configura IP estático para cabo Ethernet.
  - `type: "status"`: retorna status da rede e resultados de ping.
  - `type: "teste"`: executa teste de ping com log detalhado.
  - `type: "manutencao"`: modo placeholder de manutenção.

---

## 📡 Exemplo de Payload Bluetooth

```json
{
  "type": "wi-fi",
  "ssid": "MinhaRede",
  "password": "senha123",
  "ip": "192.168.0.100",
  "mask": "255.255.255.0",
  "gateway": "192.168.0.1"
}
```

---

## 🛠️ Instalação do Bluetooth SPP no Rock Pi

Execute o script `setup-bluetooth-spp.sh` no seu dispositivo Rock Pi S para configurar o ambiente Bluetooth:

```bash
chmod +x setup-bluetooth-spp.sh
./setup-bluetooth-spp.sh
```

Este script irá:

1. Instalar pacotes Bluetooth necessários.
2. Corrigir configurações de hostname e daemon.
3. Ativar pareamento automático via `bluetoothctl`.
4. Registrar o perfil SPP no SDP.
5. Preparar o sistema para receber conexões RFCOMM.

---

## 🧪 Testando a Comunicação

1. Emparelhe seu dispositivo Android ou PC com o Rock Pi via Bluetooth.
2. Conecte-se via terminal Bluetooth serial.
3. Envie o JSON de configuração.
4. Aguarde a resposta no terminal.

---

## 🗃️ Estrutura de Arquivos

```
├── 📁 application
│   ├── 🐍 main.py
│   └── 📄 setup.py.old
├── 📁 config
│   ├── 🐍 base_config.py
│   ├── 🐍 cable_config.py
│   ├── 🐍 integracoes_handler.py
│   ├── 🐍 maintenance_handler.py
│   ├── 🐍 status_handler.py
│   ├── 🐍 test_handler.py
│   └── 🐍 wifi_config.py
├── 📁 installers
│   ├── 📄 bluetooth-server.service
│   ├── 📄 main
│   ├── 📄 setup-bluetooth-spp.sh
│   └── 📄 setup.old
├── 📁 services
│   ├── 🐍 bluetooth_server.py
│   ├── 🐍 tcp_client.py
│   └── 🐍 udp_listener.py
├── ⚙️ .gitignore
├── 📄 LICENSE
└── 📝 README.md
```

---

## 📝 Requisitos

- Python 3
- PyBluez (`bluetooth`)
- netifaces
- `nmcli` (NetworkManager)
- `bluez` instalado e configurado

---

## 📍 Observações

- A aplicação usa `sudo` para comandos de rede. Execute como root ou configure permissões.
- O serviço Bluetooth deve estar em modo `--compat` e com o perfil `SP` (Serial Port) registrado no SDP.
- A comunicação acontece pelo canal RFCOMM 1.

---

## 📖 Licença

Projeto de uso interno. Para mais informações, entre em contato com o responsável técnico.

---