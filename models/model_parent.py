from exception_messages import *
from abc import ABC, abstractmethod
from enums.model_family import ModelFamily
from enums.input_type import InputType
from enums.constraint_input_mode import ConstraintInputMode
from exception_messages import *
import time


class Model:
    def __init__(self, name: str, model_family: ModelFamily, input_type: InputType,
                 input_mode: ConstraintInputMode,
                 input_count: int, output_type):
        """Abstract model class"""
        # the constraint that is utilizing the model
        self.constraint = None

        # the name of the model
        self.name = name

        # value to determine if the model is for a combined constraint or a normal one
        self.model_family = model_family

        # the type of input the model requires (CONSTRAINT, BOOL, INT, etc)
        self.input_type = input_type

        # how the model retrieves its data (USER, PRE-DEF, etc)
        self.input_mode = input_mode

        # number of inputs of the model requires
        self.input_count = input_count

        # the type of the output that will be returned (BOOL, INT, STRING, etc)
        self.output_type = output_type

        # output produced by model
        self.output = None

        # Specifies whether the input count can be overwritten. This
        # value can only be set for model's with a PRE_DEF input mode
        self.growable = False

        # Preventing incompatible input modes and types
        self._perform_input_safety_check()

    def _perform_input_safety_check(self):
        """This method ensures that certain input type and mode combinations are not permitted.

        A model with input mode other than MIXED_USER_PRE_DEF cannot have an input type of
        LIST_AND_BOOL, LIST_AND_INT, etc"""
        if self.input_type == InputType.LIST_AND_BOOL and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_CONSTRAINT and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_INT and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_STRING and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)

    # Utility methods
    # ---------------
    def pause(self, seconds):
        """Pause the threads by the seconds arg."""
        if type(seconds) != int:
            raise Exception("Invalid argument type passed (int type required)")

        time.sleep(seconds)

    def abort(self):
        """Stop the constraint"""
        self._complete(None)
        return -1

    def set_input_count(self, input_count):
        """Overwrite the input count. This enables an arbitrary number of inputs to be used by a model"""
        self.input_count = input_count

    def set_input_count_growable(self):
        """Allows for an arbitrary number of inputs to be added and overwrite the
        existing input count. This method can only be used for the PRE_DEF input mode,
        other input modes need to have their input count specified."""
        if self.input_mode == ConstraintInputMode.PRE_DEF:
            self.growable = True

    # ------------------

    def set_constraint(self, constraint):
        """Set the constraint object using the model"""
        self.constraint = constraint

    @abstractmethod
    def run(self, inputs: list):
        """Method that works on the input(s) provided and produces output"""

        if self.constraint is None:
            raise Exception(CONSTRAINT_NOT_SET)

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

            # save model's output
        self.output = data
        self.constraint.output = data
        self.constraint.flag.complete_constraint()
