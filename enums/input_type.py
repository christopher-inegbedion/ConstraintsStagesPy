from enum import Enum


class InputType(Enum):
    """This describes the type of input the constraint requires. This will affect all the inputs for the model"""
    BOOL = "bool"
    INT = "int"
    STRING = "str"
    CONSTRAINT = "constraint"
    LIST_AND_BOOL = "list and bool"
    LIST_AND_INT = "list and int"
    LIST_AND_STRING = "list and str"
    LIST_AND_CONSTRAINT = "list and constraint"
    ANY = "any"
