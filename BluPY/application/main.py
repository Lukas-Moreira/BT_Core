import signal
import threading

from ..services.bluetooth_server import iniciar_servidor
from ..services.udp_listener import UdpListenerConfig

class MainApp:
    def __init__(self):
        self.main()

    def main(self):
        '''
        Main application logic, this application will:

        1) Initialize UDP listener in a separate thread.
        2) Initialize Bluetooth server.
        '''
        udp = UdpListenerConfig()
        
        signal.signal(signal.SIGINT, self.handle_sigint)

        # 1) Initialize UDP listener in a separate thread
        t_udp = threading.Thread(
            target=udp.listen_for_broadcasts,
            kwargs={"port": 9050, "bufsize": 1024},  # optional arguments
            daemon=True
        )
        t_udp.start()

        # 2) Initialize Bluetooth server (can run on main thread or another thread)
        t_bt = threading.Thread(target=iniciar_servidor, daemon=True)
        t_bt.start()
        t_bt.join()
    
    def handle_sigint(self, signum, frame):
            '''
            Handle SIGINT (Ctrl+C) signal to gracefully exit the application.

            Parameters:
                - signum: Signal number.
                - frame: Current stack frame.
            '''
            print("\n[MAIN] Signal received, exiting...")
            exit(0)

if __name__ == "__main__":
    app = MainApp()