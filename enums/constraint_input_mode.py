from enum import Enum


class ConstraintInputType(Enum):
    """This describes how the model accepts its input."""
    USER = "user"
    CONSTRAINT = "constraint"
    PRE_DEF = "pre-defined"
    MIXED_USER_PRE_DEF = "mixed_user_pre_def"
