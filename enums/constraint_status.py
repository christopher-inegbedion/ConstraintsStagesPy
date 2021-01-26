from enum import Enum


class ConstraintStatus(Enum):
    NOT_STARTED = "not started"
    ACTIVE = "active"
    COMPLETE = "complete"