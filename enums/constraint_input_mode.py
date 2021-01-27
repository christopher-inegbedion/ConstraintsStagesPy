from enum import Enum


class ConstraintInputMode(Enum):
    """This describes how the model accepts its input."""

    # input is accepted through the console
    USER = "user"

    # Input is provided from the output of a constraint. This can only be used with a
    # combined constraint model
    CONSTRAINT = "constraint"

    # input is provided through function calls
    PRE_DEF = "pre-defined"

    # Input can be provided by both function calls and the console. The first input
    # provided through this input is through a function call(PRE_DEF) and the remaining can
    # either be through the console(USER) or function calls
    MIXED_USER_PRE_DEF = "mixed_user_pre_def"
