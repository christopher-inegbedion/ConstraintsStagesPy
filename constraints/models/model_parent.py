from constraints.enums.constraint_status import ConstraintStatus
from constraints.exception_messages import *
from abc import ABC, abstractmethod
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode
from constraints.exception_messages import *
import time
import logging


class Model:
    def __init__(self, name: str, model_family: ModelFamily, input_type: InputType,
                 input_mode: ConstraintInputMode,
                 input_count: int, output_type, initial_input_required=True):
        """Abstract model class"""
        # the constraint that is utilizing the model
        self.constraint = None

        # the name of the model
        self.name = name

        # value to determine if the model is for a combined constraint or a normal one
        self.model_family = model_family

        # Determines if initial value input is required. A false value means the input_count param
        # is ignored by the model.
        self.initial_input_required = initial_input_required

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

        # Specifies if the model has been aborted
        self.aborted = False

        # Preventing incompatible input modes and types
        self._perform_input_safety_check()

    # Utility methods
    # ---------------
    def validate_and_add_user_input(self, data):
        """This method validates the data provided by the constraint user. Used for USER input mode.

        Combined input types (e.g LIST_AND_BOOL, LIST_AND_INT, etc) cannot be inputted with this function"""

        if self.input_type == InputType.BOOL:  # boolean input
            if data.lower() == "true":
                return True
            elif data.lower() == "false":
                return False
            else:
                raise Exception(INVALID_CONSTRAINT_INPUT_BOOL)

        elif self.input_type == InputType.STRING:  # string input
            if data.isspace():
                raise Exception(INVALID_CONSTRAINT_INPUT_STRING)

            return data

        elif self.input_type == InputType.INT:  # int input
            if type(data) == str:
                if data.isnumeric():
                    return int(data)
                else:
                    raise Exception(INVALID_CONSTRAINT_INPUT_INT)
            else:
                raise Exception(INVALID_CONSTRAINT_INPUT_INT)

    def validate_and_add_pre_def_input(self, data):
        """This method validates the pre-defined data provided through function calls to the constraint.
                 Used for PRE_DEF input mode."""
        if self.input_type == InputType.BOOL:  # bool input
            if type(data) != bool:
                raise Exception(INVALID_CONSTRAINT_INPUT_BOOL)
            else:
                return data

        elif self.input_type == InputType.STRING:  # string input
            if type(data) != str:
                raise Exception(INVALID_CONSTRAINT_INPUT_STRING)
            else:
                return data

        elif self.input_type == InputType.INT:  # int input
            if type(data) != int:
                raise Exception(INVALID_CONSTRAINT_INPUT_INT)
            else:
                return data

        elif self.input_type == InputType.CONSTRAINT:  # constraint input
            if data is None:
                raise Exception(INVALID_CONSTRAINT_INPUT_CONSTRAINT)

            return data

        elif self.input_type == InputType.ANY:  # any input (list)
            return data

    def request_input(self, data=None):
        """Request input from the user"""
        if data is None:
            user_input = input("input: ")
            return self.validate_and_add_user_input(user_input)
        else:
            user_input = data
            return self.validate_and_add_pre_def_input(user_input)

    def pause(self, seconds):
        """Pause the threads by the seconds arg."""
        if type(seconds) != int:
            raise Exception("Invalid argument type passed (int type required)")

        if self.constraint.flag.status == ConstraintStatus.ACTIVE:
            time.sleep(seconds)

    def abort(self, msg=""):
        """Stop the constraint"""
        if self.constraint.flag.status == ConstraintStatus.ACTIVE:
            if msg == "":
                print(f"(x) MODEL: {self.name} aborted (x)")
            else:
                print(msg)
        else:
            print(f"[Constraint: {self.constraint.name} is not active.]")

        self._complete(None, True)

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

    def check_constraint_initial_input_enabled(self, data):
        """This method ensures that the constraints used by a combined constraint model have initial
        input enabled"""
        # constraints can only be inputted into a model through function calls

        # Ensure constraints have initial input enabled if used by a combined constraint model
        if self.model_family == ModelFamily.COMBINED_CONSTRAINT:
            for constraint in data:
                if constraint.model.initial_input_required is not True:
                    raise Exception(
                        INITIAL_INPUT_REQUIRED_FOR_COMBINED_CONSTRAINT)

    def _perform_input_safety_check(self):
        """This method ensures that certain input type and mode combinations are not permitted.

        This method ensures that the constraints in a combined constraint must have initial input
        enabled.

        A model with input mode other than MIXED_USER_PRE_DEF cannot have an input type of
        LIST_AND_BOOL, LIST_AND_INT, etc"""

        # Ensure input type and mode combinations are correct
        if self.input_type == InputType.LIST_AND_BOOL and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_CONSTRAINT and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_INT and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)
        if self.input_type == InputType.LIST_AND_STRING and self.input_mode != ConstraintInputMode.MIXED_USER_PRE_DEF:
            raise Exception(INCOMPATIBLE_INPUT_TYPE_AND_MODE)

    def set_constraint(self, constraint):
        """Set the constraint object using the model"""
        self.constraint = constraint

        # edit the constraint's flag's parameters
        self.constraint.flag.initial_input_required = self.initial_input_required

    @abstractmethod
    def run(self, inputs: list):
        """Method that works on the input(s) provided and produces output"""
        if self.constraint.debug:
            logging.basicConfig(
                level=logging.DEBUG)

            logging.debug(f"[MODEL]: {self.name} model running (Required input type: {self.input_type}, "
                          f"Output type: {self.output_type})")

        # performs a check for combined constraint models to ensure their constraint's have initial input enabled
        self.check_constraint_initial_input_enabled(inputs)

        if self.constraint is None:
            raise Exception(CONSTRAINT_NOT_SET)

    @abstractmethod
    def _complete(self, data, aborted=False):
        """Method that ends the constraint.
        'aborted' argument is True if the model was aborted

        This method is called from run(...) method"""
        if aborted or self.aborted:
            self.aborted = aborted
        else:
            if self.constraint.debug:
                logging.debug(
                    f"[MODEL]: {self.name} model COMPLETE with output -> {data} ({self.constraint.name})")
                print()

            # ensure the output data is the same as the required output type
            if self.output_type == InputType.INT and type(data) != int:
                raise Exception(INVALID_OUTPUT_TYPE_INT_REQUIRED)
            elif self.output_type == InputType.STRING and type(data) != str:
                raise Exception(INVALID_OUTPUT_TYPE_STRING_REQUIRED)
            elif self.output_type == InputType.BOOL and type(data) != bool:
                raise Exception(INVALID_OUTPUT_TYPE_BOOL_REQUIRED)

        # save model's output
        self.save_output(data)
        self.constraint.flag.complete_constraint()

    def save_output(self, data):
        self.output = data
        self.constraint.output = data
