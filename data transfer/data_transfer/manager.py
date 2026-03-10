from .landing_detector import LandingDetector
from .network_check import NetworkCheck
from .mission_tracker import MissionTracker
from .rsync_manager import RsyncManager
from .api_client import ApiClient
from .utils import wait


class TransferManager:

    def __init__(self):

        self.landing = LandingDetector()
        self.network = NetworkCheck()
        self.mission = MissionTracker()
        self.rsync = RsyncManager()
        self.api = ApiClient()

        self.transfer_done = False

    def run(self):

        while True:

            if self.transfer_done:
                wait(5)
                continue

            landed = self.landing.is_landed()

            if not landed:
                wait(2)
                continue

            if not self.mission.mission_ready():
                wait(2)
                continue

            if not self.network.ping_router():
                wait(3)
                continue

            if not self.network.ssh_reachable():
                wait(3)
                continue

            mission_folder = self.mission.get_latest_mission()

            success = self.rsync.transfer(mission_folder)

            if success:
                mission_name = mission_folder.split("/")[-1]
                self.api.notify_transfer_complete(mission_name)
                self.transfer_done = True

            wait(5)