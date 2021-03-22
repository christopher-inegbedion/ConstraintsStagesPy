from enum import Enum


class ConstraintEvents(Enum):
    CONSTRAINT_STARTED = 0
    ERROR = 1
    INPUT_PASSED = 2
    CONSTRAINT_COMPLETED = 3
    OUTPUT_GENERATED = 4
