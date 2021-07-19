from enum import Enum


class StageStatus(Enum):
    NOT_STARTED = 0
    ACTIVE = 1
    CONSTRAINT_STARTED = 2
    CONSTRAINT_COMPLETED = 3
    COMPLETE = 4
    ERROR = 5
