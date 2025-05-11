from abc import ABC, abstractmethod

class BaseC2(ABC):
    @property
    @abstractmethod
    def NAME(self) -> str:
        """A short name for this C2."""
    
    @property
    @abstractmethod
    def CLIENT(self):
        """The underlying client/connection object."""
    
    def __init__(self, *args, **kwargs):
        # nothing here — everything comes from NAME/CLIENT
        super().__init__()
    
    def get_name(self):
        return self.NAME

    @abstractmethod
    def list_sessions(self):
        """Must return a list of sessions"""

    @abstractmethod
    def list_beacons(self):
        """Must return a list of beacons"""
    
    @abstractmethod
    def send_beacon_cmd(self, beacon_id, commands):
        """Must send `commands` to host `beacon_id`."""
    
    @abstractmethod
    def send_session_cmd(self, beacon_id, commands):
        """Must send `commands` to host `beacon_id`."""
