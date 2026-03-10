import os
from .config import MISSION_DATA_PATH


class MissionTracker:

    def get_latest_mission(self):

        if not os.path.exists(MISSION_DATA_PATH):
            return None

        missions = sorted(os.listdir(MISSION_DATA_PATH))

        if not missions:
            return None

        latest = missions[-1]

        return os.path.join(MISSION_DATA_PATH, latest)

    def mission_ready(self):

        mission = self.get_latest_mission()

        if mission and os.listdir(mission):
            return True

        return False