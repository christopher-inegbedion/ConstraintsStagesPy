from enum import Enum

class AdminStatus(Enum):
    """This describes the status of the admin section"""
    # The admin has not started
    NOT_STARTED = "not_started"

    # The admin has started
    STARTED = "started"

    # The admin is active
    ACTIVE = "active"

    # The admin has paused
    PAUSED = "paused"

    # The admin has completed
    COMPLETE = "complete"