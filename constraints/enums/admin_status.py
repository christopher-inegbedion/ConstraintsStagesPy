from enum import Enum

class AdminStatus(Enum):
    """This describes the status of the admin section"""
    NOT_STARTED = "not_started"

    STARTED = "started"

    ACTIVE = "active"

    PAUSED = "paused"

    COMPLETE = "complete"