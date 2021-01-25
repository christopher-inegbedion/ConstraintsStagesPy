from enums.model_family import ModelFamily
from exception_messages import *
from flag import Flag
from models.model_parent import Model
from abc import ABC, abstractmethod
from enums.input_type import InputType
from enums.constraint_input_mode import ConstraintInputType


class Constraint(ABC):
    """Abstract constraint class"""
    def __init__(self, name: str, flag: Flag, model: Model):
        """Each constraint has a flag and model

        Flag :- The flag defines the properties for the constraint
        Model :- The model defines what the constraint needs (i.e inputs),
                 what it does and what it produces

        Order of operation :- [INPUT]start() -> [MODEL]model.run([INPUT]) -> [OUTPUT]complete(data)"""
        self.name = name  # constraint name. for debugging purposes
        self.flag = flag  # constraint's flag
        self.inputs = []  # constraint's input(s)
        self.model = model  # constraint's model
        self.output = None  # constraint's output

        if self.model.model_family == ModelFamily.COMBINED_CONSTRAINT:
            self._init_constraints_in_comb_constraint()

    def _init_constraints_in_comb_constraint(self):
        """Set the properties of a constraint in a combined constraint"""
        for constraint in self.inputs:
            constraint.flag.set_combined(True)
            constraint.flag.set_required(True)

    @abstractmethod
    def start(self):
        """This method starts the constraint"""
        self.flag.start_constraint()  # initialize the constraint's flag details.

        if self.model.input_mode == ConstraintInputType.USER:
            for input_count in range(self.model.input_count):
                user_input = input("input: ")
                # validate and add the input provided by the user
                self.validate_and_add_user_input(user_input)
        elif self.model.input_mode == ConstraintInputType.PRE_DEF:
            if len(self.inputs) > self.model.input_count:
                raise Exception(INPUTS_ENTERED_MORE_THAN_REQUIRED)
        elif self.model.input_mode == ConstraintInputType.MIXED_USER_PRE_DEF:
            user_input = input("input: ")

            self.validate_and_add_user_input(user_input)

        # begin the model
        self.model.run(self.inputs)

    def validate_and_add_user_input(self, data):
        """This method validates the data provided by the constraint user. Used for USER input mode."""
        if self.model.input_type == InputType.BOOL:  # boolean input
            if data.lower() == "true":
                self.inputs.append(True)
            elif data.lower() == "false":
                self.inputs.append(False)
            else:
                raise Exception(INVALID_CONSTRAINT_INPUT_BOOL)

        elif self.model.input_type == InputType.STRING:  # string input
            if data.isspace():
                raise Exception(INVALID_CONSTRAINT_INPUT_STRING)

            self.inputs.append(data)

        elif self.model.input_type == InputType.INT:  # int input
            if type(data) == str:
                if data.isnumeric():
                    self.inputs.append(int(data))
            else:
                raise Exception(INVALID_CONSTRAINT_INPUT_INT)

        elif self.model.input_type == InputType.ANY:  # any input (list)
            self.inputs.append(data)

    def validate_and_add_predef_input(self, data):
        """This method validates the data provided by the constraint. Used for PRE_DEF input mode."""
        if self.model.input_type == InputType.BOOL:  # bool input
            if type(data) != bool:
                raise Exception(INVALID_CONSTRAINT_INPUT_BOOL)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.STRING:  # string input
            if type(data) != str:
                raise Exception(INVALID_CONSTRAINT_INPUT_STRING)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.INT:  # int input
            if type(data) != int:
                raise Exception(INVALID_CONSTRAINT_INPUT_INT)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.CONSTRAINT:  # constraint input
            if data is None:
                raise Exception(INVALID_CONSTRAINT_INPUT_CONSTRAINT)

            self.inputs.append(data)

        elif self.model.input_type == InputType.ANY:  # any input (list)
            self.inputs.append(data)

    def add_input(self, data):
        """Add input to the constraint. This method is only used if the input mode is PRE_DEF or MIXED_USER_PRE_DEF"""

        if self.model.input_mode == ConstraintInputType.PRE_DEF \
                or self.model.input_mode == ConstraintInputType.MIXED_USER_PRE_DEF:
            # verify the input provided
            self.validate_and_add_predef_input(data)
        else:
            raise Exception(MANUAL_INPUT_NOT_ALLOWED)



