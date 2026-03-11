from pymavlink import mavutil
from config import MAVLINK_CONNECTION


class LandingDetector:

    def __init__(self):
        self.master = mavutil.mavlink_connection(MAVLINK_CONNECTION)

    def is_landed(self):
        self.extended_sys_state_msg_id = 245
        # Request EXTENDED_SYS_STATE messages at 1 Hz
        self.interval_us = 1000000
        # Send the COMMAND_LONG message
        self.master.mav.command_long_send(
            self.master.target_system,    # Target system (typically 1)
            self.master.target_component, # Target component (typically 0 or MAV_COMP_ID_AUTOPILOT1)
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, # Command (511)
            0,                       # Confirmation
            self.extended_sys_state_msg_id,                  # param1: Message ID
            self.interval_us,             # param2: Interval in microseconds
            0, 0, 0, 0, 0            # param3-7: Not used
        )

        # Get landing state
        msg = self.master.recv_match(type='EXTENDED_SYS_STATE', blocking=True).to_dict()

        if msg is None:
            return False

        landed = msg['landed_state'] == 1

        # Drone must be landed AND disarmed
        if landed:
            return True
        return False
    
    def is_armed(self):
        self.heartbeat_msg_id = 0
        # Request EXTENDED_SYS_STATE messages at 1 Hz
        self.interval_us = 1000000
        # Send the COMMAND_LONG message
        self.master.mav.command_long_send(
            self.master.target_system,    # Target system (typically 1)
            self.master.target_component, # Target component (typically 0 or MAV_COMP_ID_AUTOPILOT1)
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, # Command (511)
            0,                       # Confirmation
            self.heartbeat_msg_id,       # param1: Message ID
            self.interval_us,             # param2: Interval in microseconds
            0, 0, 0, 0, 0            # param3-7: Not used
        )
        # Get heartbeat to check armed state
        hb = self.master.recv_match(type='HEARTBEAT', blocking=True).to_dict()

        if hb is None:
            return False

        disarmed = hb['base_mode'] != 128

        return disarmed
    
    def is_ready_for_data_transfer(self):
        return self.is_landed() and self.is_armed()
    
if __name__ == "__main__":
    detector = LandingDetector()
    while True:
        if detector.is_ready_for_data_transfer():
            print("Drone is ready for data transfer.")
        else:
            print("Drone is not ready for data transfer.")