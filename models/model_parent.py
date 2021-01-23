from abc import ABC, abstractmethod
from enums.model_family import ModelFamily
from enums.input_type import InputType
from enums.constraint_input_type import ConstraintInputType
# from constraint import Constraint


class Model:

    def __init__(self, name: str, model_family: ModelFamily, input_type: InputType,
                 input_mode: ConstraintInputType,
                 input_count: int, output_type):
        self.constraint = None  # the constraint that is utilizing the model
        self.name = name  # the name of the model
        self.model_family = model_family  # value to determine if the model is for a combined constraint or a normal one
        self.input_type = input_type  # the type of input the model requires (CONSTRAINT, BOOL, INT, etc)
        self.input_mode = input_mode  # how the model retrieves its data (USER, PRE-DEF, etc)
        self.input_count = input_count  # number of inputs of the model requires
        self.output_type = output_type  # the type of the output that will be returned (BOOL, INT, STRING, etc)
        self.output = None


    def set_constraint(self, constraint):
        self.constraint = constraint

    @abstractmethod
    def run(self, inputs: list):
        pass

    @abstractmethod
    def _complete(self, data):  # call this method last in custom models
        # ensure the output data is the same as the required output type
        if self.output_type == InputType.INT and type(data) != int:
            raise Exception("Invalid output type (Output type specified -> INT)")
        elif self.output_type == InputType.STRING and type(data) != str:
            raise Exception("Invalid output type (Output type specified -> STRING)")
        elif self.output_type == InputType.BOOL and type(data) != bool:
            raise Exception("Invalid output type (Output type specified -> BOOL)")
        self.constraint.flag.complete_constraint()
