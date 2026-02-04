#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y rockchip-overlay
sudo apt-get install -y linux-4.4-rockpis-latest
sudo apt-get install -y rtl8723ds-firmware
sudo apt-get install -y bluez

cat /sys/class/net/wlan0/address | sudo tee /opt/bdaddr > /dev/null

if [ ! -f /opt/bdaddr ]; then
  echo "⚠️  Aviso: arquivo /opt/bdaddr não encontrado. Verifique a instalação do firmware."
  exit 1
fi

sudo hostnamectl set-hostname "Coletor_$(cat /sys/class/net/wlan0/address)"

echo "🔧 [1/8] Corrigindo erro de hostname..."
HOSTNAME=$(hostname)
if ! grep -q "$HOSTNAME" /etc/hosts; then
  echo "127.0.1.1   $HOSTNAME" | sudo tee -a /etc/hosts
fi

echo "🔧 [2/8] Ativando bluetoothd em modo compatível..."
sudo mkdir -p /etc/systemd/system/bluetooth.service.d
cat <<EOF | sudo tee /etc/systemd/system/bluetooth.service.d/override.conf >/dev/null
[Service]
ExecStart=
ExecStart=/usr/lib/bluetooth/bluetoothd --compat
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart bluetooth.service

echo "🔧 [3/8] Criando serviço bluetooth-agent.service (pareamento automático)..."
cat <<EOF | sudo tee /etc/systemd/system/bluetooth-agent.service >/dev/null
[Unit]
Description=Bluetooth Agent auto-pairing
After=bluetooth.service
Requires=bluetooth.service

[Service]
ExecStart=/bin/bash -c 'sleep 2 && bluetoothctl power on && bluetoothctl discoverable on && bluetoothctl pairable on && bluetoothctl agent NoInputNoOutput && bluetoothctl default-agent'
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable bluetooth-agent.service
sudo systemctl start bluetooth-agent.service

echo "🧹 [4/8] Removendo rfcomm.service (porta serial), não será mais usado..."
sudo systemctl stop rfcomm.service || true
sudo systemctl disable rfcomm.service || true
sudo rm -f /etc/systemd/system/rfcomm.service

echo "🔧 [5/8] Garantindo que o módulo rfcomm esteja carregado (ainda útil para suporte geral)..."
sudo modprobe rfcomm
if ! grep -q "^rfcomm" /etc/modules; then
  echo "rfcomm" | sudo tee -a /etc/modules
fi

echo "🔧 [6/8] Criando serviço bluetooth-sdp.service (registro SPP no SDP)..."
cat <<EOF | sudo tee /etc/systemd/system/bluetooth-sdp.service >/dev/null
[Unit]
Description=Bluetooth SDP SP Profile
After=bluetooth.service
Requires=bluetooth.service

[Service]
ExecStart=/usr/bin/sdptool add --channel=1 SP
Type=oneshot

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable bluetooth-sdp.service
sudo systemctl start bluetooth-sdp.service

echo "📡 [7/8] Verificando anúncio SPP via SDP..."
sudo sdptool browse local | grep -A5 "Serial Port" || echo "⚠️  Aviso: perfil SPP ainda não detectado no SDP."

echo "📡 [8/8] Iniciando servidor..."
sudo mv main /usr/bin/
sudo chmod +x /usr/bin/main
sudo mv bluetooth-server.service /etc/systemd/system/
sudo systemctl start bluetooth-server.service
sudo systemctl enable bluetooth-server.service

echo "✅ Configuração concluída!"
echo "O Rock Pi está pronto para receber pareamentos e conexões via socket RFCOMM (main)."