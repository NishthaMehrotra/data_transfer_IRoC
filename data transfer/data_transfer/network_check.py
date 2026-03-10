import socket
import subprocess
from .config import BASE_STATION_IP, SSH_PORT, PING_TIMEOUT


class NetworkCheck:

    def ping_router(self):

        try:
            subprocess.check_output(
                ["ping", "-c", "1", "-W", str(PING_TIMEOUT), BASE_STATION_IP]
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def ssh_reachable(self):

        try:
            sock = socket.create_connection(
                (BASE_STATION_IP, SSH_PORT),
                timeout=3
            )
            sock.close()
            return True

        except Exception:
            return False