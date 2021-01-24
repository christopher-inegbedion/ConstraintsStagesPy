from exception_messages import *
from abc import ABC, abstractmethod
from enums.model_family import ModelFamily
from enums.input_type import InputType
from enums.constraint_input_type import ConstraintInputType


class Model:
    def __init__(self, name: str, model_family: ModelFamily, input_type: InputType,
                 input_mode: ConstraintInputType,
                 input_count: int, output_type):
        """Abstract model class"""
        self.constraint = None  # the constraint that is utilizing the model
        self.name = name  # the name of the model
        self.model_family = model_family  # value to determine if the model is for a combined constraint or a normal one
        self.input_type = input_type  # the type of input the model requires (CONSTRAINT, BOOL, INT, etc)
        self.input_mode = input_mode  # how the model retrieves its data (USER, PRE-DEF, etc)
        self.input_count = input_count  # number of inputs of the model requires
        self.output_type = output_type  # the type of the output that will be returned (BOOL, INT, STRING, etc)
        self.output = None  # output produced by model

        if model_family == ModelFamily.COMBINED_CONSTRAINT:
            self.init_constraints_in_comb_constraint()

    def set_constraint(self, constraint):
        """Set the constraint object using the model"""
        self.constraint = constraint

    def init_constraints_in_comb_constraint(self):
        """Set the properties of a constraint in a combined constraint"""
        for constraint in self.constraint.inputs:
            constraint.flag.set_combined(True)
            constraint.flag.set_required(True)

    @abstractmethod
    def run(self, inputs: list):
        """Method that works on the input(s) provided and produces output"""
        pass

    @abstractmethod
    def _complete(self, data):  # call this method last in custom models
        """Method that ends the constraint. Called from run(...) method"""

        # ensure the output data is the same as the required output type
        if self.output_type == InputType.INT and type(data) != int:
            raise Exception(INVALID_OUTPUT_TYPE_INT_REQUIRED)
        elif self.output_type == InputType.STRING and type(data) != str:
            raise Exception(INVALID_OUTPUT_TYPE_STRING_REQUIRED)
        elif self.output_type == InputType.BOOL and type(data) != bool:
            raise Exception(INVALID_OUTPUT_TYPE_BOOL_REQUIRED)

        self.constraint.flag.complete_constraint()
