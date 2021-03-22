from enum import Enum


class StageEvents(Enum):
    STARTED = 1
    CONSTRAINT_STARTED = 2
    CONSTRAINT_COMPLETED = 3
    COMPLETED = 4
