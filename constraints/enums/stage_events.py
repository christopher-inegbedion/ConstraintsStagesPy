from enum import Enum


class StageEvents(Enum):
    STAGE_STARTED = 1
    STAGE_CONSTRAINT_STARTED = 2
    STAGE_CONSTRAINT_COMPLETED = 3
    STAGE_COMPLETED = 4
