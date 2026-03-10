from pymavlink import mavutil
from .config import MAVLINK_CONNECTION


class LandingDetector:

    def __init__(self):
        self.master = mavutil.mavlink_connection(MAVLINK_CONNECTION)

    def is_landed(self):

        # Get landing state
        msg = self.master.recv_match(type='EXTENDED_SYS_STATE', blocking=True)

        if msg is None:
            return False

        landed = (
            msg.landed_state ==
            mavutil.mavlink.MAV_LANDED_STATE_ON_GROUND
        )

        # Get heartbeat to check armed state
        hb = self.master.recv_match(type='HEARTBEAT', blocking=True)

        if hb is None:
            return False

        armed = bool(
            hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
        )

        # Drone must be landed AND disarmed
        if landed and not armed:
            return True

        return False