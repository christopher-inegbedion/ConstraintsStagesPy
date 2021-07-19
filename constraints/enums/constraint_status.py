from enum import Enum


class ConstraintStatus(Enum):
    """This describes the status of the constraint/model"""

    # constraint/model has not been started
    NOT_STARTED = "not started"

    # model is doing some work
    ACTIVE = "active"

    # model has been paused
    PAUSED = "paused"

    # model is waiting for external input
    PENDING_INPUT = "pending_input"

    # model has completed work and its output has been saved
    COMPLETE = "complete"
