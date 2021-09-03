from enum import Enum


class StageStatus(Enum):
    """The status of the stage"""

    # The stage has not started
    NOT_STARTED = 0

    # The stage has started and is active
    ACTIVE = 1

    # A constraint in the stage has started
    CONSTRAINT_STARTED = 2

    # A constraint in the stage has completed
    CONSTRAINT_COMPLETED = 3

    # The stage has completed
    COMPLETE = 4

    # The stage encountered an error
    ERROR = 5
