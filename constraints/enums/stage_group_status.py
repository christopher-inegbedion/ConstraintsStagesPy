from enum import Enum

class StageGroupEnum(Enum):
    """Defines the status of the StageGroup"""
    # The stage group has not started
    NOT_STARTED = 1

    # A stage in the stage group is running
    RUNNING = 2

    # The stage group has completed
    COMPLETE = 3