from enum import Enum


class ConstraintInputType(Enum):
    """This describes how the model accepts its input."""
    USER = "user"
    CONSTRAINT = "constraint"
    PRE_DEF = "pre-defined"