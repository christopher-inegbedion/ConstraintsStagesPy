from enum import Enum


class ModelFamily(Enum):
    """This describes if the constraint is combined or normal"""
    COMBINED_CONSTRAINT = "combined_constraint"
    CONSTRAINT = "constraint"
