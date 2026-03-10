import subprocess
from .config import BASE_STATION_IP, BASE_STATION_USER, BASE_STATION_DATA_PATH


class RsyncManager:

    def transfer(self, mission_folder):

        destination = f"{BASE_STATION_USER}@{BASE_STATION_IP}:{BASE_STATION_DATA_PATH}"

        cmd = [
            "rsync",
            "-avz",
            mission_folder,
            destination
        ]

        try:
            subprocess.check_call(cmd)
            return True

        except subprocess.CalledProcessError:
            return False