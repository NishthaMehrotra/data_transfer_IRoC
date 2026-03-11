from rsync import Rsync
from .config import BASE_STATION_IP, BASE_STATION_USER, BASE_STATION_DATA_PATH


class RsyncManager:

    def transfer(self, mission_folder):

        destination = f"{BASE_STATION_USER}@{BASE_STATION_IP}:{BASE_STATION_DATA_PATH}"

        try:
            rsync = Rsync(
                source=mission_folder,
                destination=destination,
                options=["-avz", "--progress", "--partial"]
            )

            rsync.run()

            return True

        except Exception as e:
            print("Rsync failed:", e)
            return False