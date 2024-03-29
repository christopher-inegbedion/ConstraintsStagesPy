from enum import Enum


class InputType(Enum):
    """This describes the type of input the constraint requires."""
    BOOL = "bool"
    INT = "int"
    STRING = "str"
    CONSTRAINT = "constraint"
    LIST_AND_BOOL = "list and bool"
    LIST_AND_INT = "list and int"
    LIST_AND_STRING = "list and str"
    LIST_AND_CONSTRAINT = "list and constraint"
    TASK = "task"
    ANY = "any"
