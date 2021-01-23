from enum import Enum


class InputType(Enum):
    """This describes the type of input the constraint requires. This will affect all the inputs for the model"""
    BOOL = "bool"
    INT = "int"
    STRING = "str"
    CONSTRAINT = "constraint"