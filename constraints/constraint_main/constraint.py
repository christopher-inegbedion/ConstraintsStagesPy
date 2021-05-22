from constraints.constraint_main.constraint_log import ConstraintLog
from constraints.enums.constraint_status import ConstraintStatus
from constraints.enums.model_family import ModelFamily
from constraints.exception_messages import *
from constraints.constraint_main.flag import Flag
from constraints.models.model_parent import Model
from abc import ABC, abstractmethod
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode
import logging


class Constraint(ABC):
    """Abstract constraint class"""

    def __init__(self, name: str, description: str, flag: Flag, model: Model, debug=False):
        """Each constraint has a flag and model

        Flag :- The flag defines the properties for the constraint
        Model :- The model defines what the constraint needs (i.e inputs),
                 what it does and what it produces

        Order of operation :- [INPUT]start() -> [MODEL]model.run([INPUT]) -> [OUTPUT]complete(data)"""
        self.name = name  # constraint name
        self.description = description  # constraint's description
        self.flag: Flag = flag  # constraint's flag
        self.inputs = []  # constraint's input(s)
        self.model = model  # constraint's model
        self.output = None  # constraint's output
        self.debug = debug  # determines if debug messages will be displayed
        self.task_instance = None  # constraint's task
        self.stage = None

        # support for providing custom flags
        if flag is not None:
            self.flag = flag
        else:
            self.flag = Flag("ConstraintVerification",
                             ConstraintStatus.NOT_STARTED, False, False, False, "", "")
        self.flag.set_constraint(self)

        # initialize the flag params for the constraints in the combined constraint's constraints
        if self.model.model_family == ModelFamily.COMBINED_CONSTRAINT:
            self._init_constraints_in_comb_constraint()

        self.model.set_constraint(self)

    def _init_constraints_in_comb_constraint(self):
        """Set the properties of a constraint in a combined constraint"""
        for constraint in self.inputs:
            constraint.flag.set_combined(True)
            constraint.flag.set_required(True)

    @abstractmethod
    def start(self, d: bool = False):
        """This method starts the constraint. This is where the inputs are retrieved and passed to the model"""
        self.debug = d
        # initialize the constraint's flag details.

        # display debug info.
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug(f"[CONSTRAINT]: {self.name} running")

        if self.model.initial_input_required:
            # Accept the inputs. Before the model is run the inputs provided have
            # to be verified for each input mode.
            # ---------------

            # Input is entered directly from the console
            if self.model.input_mode == ConstraintInputMode.USER:
                for input_count in range(self.model.input_count):
                    user_input = input("input: ")
                    # validate and add the input provided by the user
                    self.validate_and_add_user_input(user_input)

            # Input is entered through the use of function calls
            elif self.model.input_mode == ConstraintInputMode.PRE_DEF:
                # Some models can be set as growable, and thus multiple function calls to add an input
                # can be called that are less or more than the model's pre-set input count
                if self.model.growable:
                    input_count = len(self.inputs)
                    self.model.input_count = input_count
                else:
                    if len(self.inputs) > self.model.input_count or len(self.inputs) < self.model.input_count:
                        raise self._raise_exception(
                            INSUFFICIENT_AMOUNT_OF_INPUTS_ENTERED)

            # Input can be entered through the console and function calls. For this
            # input mode, the first input has to be a pre-defined value and the remaining
            # inputs user defined (i.e from the console)
            elif self.model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
                # The first input received by the constraint is the pre-defined input
                # and the remaining (if the input_count > 1) will be user defined.
                if self.model.input_count-1 >= 1:
                    for input_count in range(self.model.input_count-1):
                        user_input = input("input: ")

                        self.validate_and_add_user_input(user_input)

            self.flag.start_constraint(self.inputs)

        # begin the model
        self.model.run(self.inputs)
        self.inputs.clear()

    def get_model_input_type(self):
        """Return the type of input required"""
        return self.model.input_type

    def pause(self):
        """Pause the constraint"""
        if self.get_status() == ConstraintStatus.ACTIVE:
            self.model.pause()

    def get_task_instance(self):
        """Return the constraint's task instance"""
        return self.task_instance

    def set_task_instance(self, task):
        """Sets the constraint's Task"""
        self.task_instance = task

    def get_status(self) -> ConstraintStatus:
        return self.flag.status

    def validate_and_add_user_input(self, data):
        """This method validates the data provided by the constraint user. Used for USER input mode."""
        if self.model.input_type == InputType.BOOL:  # boolean input
            if data.lower() == "true":
                self.inputs.append(True)
            elif data.lower() == "false":
                self.inputs.append(False)
            else:
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_BOOL)

        elif self.model.input_type == InputType.STRING:  # string input
            if data.isspace():
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_STRING)

            self.inputs.append(data)

        elif self.model.input_type == InputType.INT:  # int input
            if type(data) == str:
                if data.isnumeric():
                    self.inputs.append(int(data))
                else:
                    raise self._raise_exception(INVALID_CONSTRAINT_INPUT_INT)
            else:
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_INT)

        elif self.model.input_type == InputType.LIST_AND_BOOL:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be booleans

            # ensure that the first input has been entered before the console input is entered
            if self.inputs == []:
                raise self._raise_exception(CONSTRAINT_INPUT_ORDER_MISMATCH)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_STRING:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be booleans

            # ensure that the first input has been entered before the console input is entered
            if self.inputs == []:
                raise self._raise_exception(CONSTRAINT_INPUT_ORDER_MISMATCH)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_INT:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be ints

            # ensure that the first input has been entered before the console input is entered
            if self.inputs == []:
                raise self._raise_exception(CONSTRAINT_INPUT_ORDER_MISMATCH)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_CONSTRAINT:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.

            # A constraint cannot be entered through the console
            pass

    def validate_and_add_predef_input(self, data):
        """This method validates the pre-defined data provided through function calls to the constraint.
         Used for PRE_DEF input mode."""
        if self.model.input_type == InputType.BOOL:  # bool input
            if type(data) != bool:
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_BOOL)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.STRING:  # string input
            if type(data) != str:
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_STRING)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.INT:  # int input
            if type(data) != int:
                raise self._raise_exception(INVALID_CONSTRAINT_INPUT_INT)
            else:
                self.inputs.append(data)

        elif self.model.input_type == InputType.CONSTRAINT:  # constraint input
            if data is None:
                raise self._raise_exception(
                    INVALID_CONSTRAINT_INPUT_CONSTRAINT)

            self.inputs.append(data)

        elif self.model.input_type == InputType.ANY:  # any input (list)
            self.inputs.append(data)

        # combined input types
        # --------------------
        elif self.model.input_type == InputType.LIST_AND_BOOL:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be booleans

            # ensure that only a single pre-defined input can be stored
            if len(self.inputs) == 1:
                raise self._raise_exception(PRE_DEF_INPUTS_ALREADY_EXISTING)
            elif type(data) != list:
                raise self._raise_exception(
                    MIXED_USER_PRE_DEF_FIRST_INPUT_MUST_BE_LIST)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_STRING:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be booleans

            # ensure that only a single pre-defined input can be stored
            if len(self.inputs) == 1:
                raise self._raise_exception(PRE_DEF_INPUTS_ALREADY_EXISTING)
            elif type(data) != list:
                raise self._raise_exception(
                    MIXED_USER_PRE_DEF_FIRST_INPUT_MUST_BE_LIST)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_INT:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be ints

            # ensure that only a single pre-defined input can be stored
            if len(self.inputs) == 1:
                raise self._raise_exception(PRE_DEF_INPUTS_ALREADY_EXISTING)
            elif type(data) != list:
                raise self._raise_exception(
                    MIXED_USER_PRE_DEF_FIRST_INPUT_MUST_BE_LIST)

            self.inputs.append(data)
        elif self.model.input_type == InputType.LIST_AND_CONSTRAINT:  # a list and bool combination
            # This type of input can only be used if the input mode of the model is mixed.
            # The first input is a list with some values and the remaining inputs will be constraint

            # ensure that only a single pre-defined input can be stored
            if len(self.inputs) == 1:
                raise self._raise_exception(PRE_DEF_INPUTS_ALREADY_EXISTING)
            elif type(data) != list:
                raise self._raise_exception(
                    MIXED_USER_PRE_DEF_FIRST_INPUT_MUST_BE_LIST)

            self.inputs.append(data)

    def add_input(self, data):
        """Add input to the constraint. This method is only used if the input mode is PRE_DEF or MIXED_USER_PRE_DEF"""

        if self.model.initial_input_required:
            if self.model.input_mode == ConstraintInputMode.PRE_DEF \
                    or self.model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
                self.validate_and_add_predef_input(data)
            else:
                raise self._raise_exception(MANUAL_INPUT_NOT_ALLOWED)
        else:
            raise self._raise_exception(INITIAL_INPUT_NOT_ENABLED)

    def show_constraint_stage_not_active_err_msg(self):
        print(
            f"[Constraint {self.name} cannot start. Its stage has not begun]")

    def set_stage(self, stage):
        self.stage = stage
        self.flag.log.attach(stage)

        # Child constraint's have to be passed the stage object manually
        if self.model.model_family == ModelFamily.COMBINED_CONSTRAINT:
            for constraint in self.inputs:
                constraint.set_stage(stage)

    def _raise_exception(self, exception_msg) -> Exception:
        self.inputs.clear()
        self.flag.log_error(exception_msg)
        return Exception(exception_msg)
