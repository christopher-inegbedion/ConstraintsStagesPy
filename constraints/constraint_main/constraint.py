from time import sleep
from constraints.enums.admin_status import AdminStatus
import threading
from typing import Any
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

    def __init__(self, name: str, description: str, flag: Flag, model: Model, is_admin_input_required, debug=False, completion_data_labels=[]):
        """Each constraint has a flag and model

        Flag :- The flag defines the properties for the constraint
        Model :- The model defines what the constraint needs (i.e inputs),
                 what it does and what it produces

        Order of operation :- [INPUT]start() -> [MODEL]run([INPUT]) -> [OUTPUT]complete(data)

        The admin model[start_admin()] can also be started """

        # constraint name
        self.name = name

        # constraint's description
        self.description = description

        # constraint's flag
        self.flag: Flag = flag

        # constraint's input(s)
        self.inputs = []
        
        # Defines if the constraint's admin will be providing any input to the constraint
        self.is_admin_input_required = is_admin_input_required

        # The titles of each completion data.This is used
        self.completion_data_labels = completion_data_labels

        # This variable is used when the model completes to store analytics information
        self.completion_data = {}
        
        # constraint's configuration inputs
        self.configuration_inputs = {}

        # constraint's model
        self.model = model

        # constraint's output
        self.output = None

        # determines if debug messages will be displayed
        self.debug = debug

        # constraint's task
        self.task_instance = None

        # The constraint's current stage
        self.stage = None

        # To keep track of the number of configuration inputs have been inputted
        self._config_params_entered = 0

        # The status of the model's admin function
        self.admin_status = AdminStatus.NOT_STARTED

        # The function runs when the model calls the external action function. This is set
        # with the on_external_action(..) function
        self.external_action_func = None

        self.external_action_args = None

        # This function runs when the self.confiuration_inputs variable is modified. This is
        # set with the on_config_action(..) function
        self.notify_config_action_func = None

        self.listen_msg = None
        self.listen_data = None
        self.listen_msg_lock = threading.Lock()

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

        if self.model.initial_input_required:
            # Accept the inputs. Before the model is run, the inputs provided have
            # to be verified for each input mode.
            # ---------------

            # Input is entered directly from the console
            if self.model.input_mode == ConstraintInputMode.USER:
                for input_count in range(self.model.input_count):
                    user_input = input("input: ")
                    # validate and add the input provided by the user
                    self._validate_and_add_user_input(user_input)

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
                            INSUFFICIENT_AMOUNT_OF_INPUTS_ENTERED, extra_info=f"Inputs entered: {self.inputs}")

            # Input can be entered through the console and function calls. For this
            # input mode, the first input has to be a pre-defined value and the remaining
            # inputs user defined (i.e from the console)
            elif self.model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
                # The first input received by the constraint is the pre-defined input
                # and the remaining (if the input_count > 1) will be user defined.
                if self.model.input_count-1 >= 1:
                    for input_count in range(self.model.input_count-1):
                        user_input = input("input: ")

                        self._validate_and_add_user_input(user_input)

        # Verify the model's configuration inputs
        if self.model.configuration_input_required:
            number_of_configuration_inputs = len(self.configuration_inputs)

            if number_of_configuration_inputs == 0 and self.model.configuration_input_count == 99:
                # This condition should not trigger an error, because keeping the configuration input count at the default
                # value -> 99 would mean that the model does not really need the configuration inputs, and a default value can be
                # used in the case where the inputs are not entered
                pass
            elif number_of_configuration_inputs != self.model.configuration_input_count:
                raise self._raise_exception(INSUFFICIENT_CONFIGURATION_INPUTS_ENTERED,
                                            extra_info=f"Required amount: {self.model.configuration_input_count}, amount provided: {number_of_configuration_inputs}, data: {self.configuration_inputs}")
            elif number_of_configuration_inputs > self.model.configuration_input_count:
                raise self._raise_exception(
                    EXCESSIVE_CONFIGURATION_INPUTS_ENTERED)

        self.flag.start_constraint(self.inputs)

        # begin the model
        self.model.run(
            self.inputs, configuration_inputs=self.configuration_inputs)

        # self.model.run_admin(self.inputs)
        self.inputs.clear()

    def start_admin(self):
        """This method starts the admin model. It can only be started after the main model function has started."""

        # This is to prevent the model's main function and this function from colliding
        # in the case where they are started at the same time
        sleep(1)

        # The model's admin function is run in a seperate thread to enable the
        # model's main function and admin function run simultaneously
        admin_func_thread = threading.Thread(target=self.model.run_admin,
                                             name=f"{self.model.name}-Admin")

        # The variable [self.model.admin_session_independent] describes whether the main
        # function and the admin function can be active at the same time
        main_model_status = self.flag.status
        if self.model.admin_session_independent:
            while True:
                if main_model_status != ConstraintStatus.NOT_STARTED:
                    main_model_status = AdminStatus.ACTIVE

                    admin_func_thread.run()
                    main_model_status = AdminStatus.COMPLETE
                    break
        else:
            while True:
                if main_model_status == ConstraintStatus.PAUSED and self.admin_status != AdminStatus.COMPLETE:
                    self.admin_status = AdminStatus.ACTIVE
                    admin_func_thread.run()
                    self.admin_status = AdminStatus.COMPLETE
                    break

    # def start_listen(self):
    #     threading.Thread(target=self._start_listen, daemon=True).start()

    # def _start_listen(self):
    #     while True:
    #         with self.listen_msg_lock:
    #             self.model.listen()

    def get_listen_msg(self):
        return self.listen_msg

    def send_listen_data(self, msg: str, data):
        self.listen_msg = msg
        self.listen_data = data
        self.model.listen(msg, data)

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

    def _validate_and_add_user_input(self, data):
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

    def _validate_and_add_predef_input(self, data):
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
        self.flag.set_status(ConstraintStatus.INPUT_PASSED, data)

    def add_input(self, data, admin=False):
        """Add input to the constraint. This method is only used if the input mode is PRE_DEF or MIXED_USER_PRE_DEF"""

        if admin is False:
            if self.model.configuration_input_required and self.model.config_parameters == []:
                raise Exception("Config parameters are required. ")

            if self.model.initial_input_required:
                if self.model.input_mode == ConstraintInputMode.PRE_DEF \
                        or self.model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
                    self._validate_and_add_predef_input(data)
                else:
                    raise self._raise_exception(MANUAL_INPUT_NOT_ALLOWED)
            else:
                raise self._raise_exception(INITIAL_INPUT_NOT_ENABLED)
        else:
            if data != None:
                self.inputs.append(data)

    def add_configuration_input(self, data, key=None, validation_req=True):
        if self.model.configuration_input_required or validation_req == False:
            if len(self.configuration_inputs) >= self.model.configuration_input_count:
                raise self._raise_exception(
                    f"The maximum number of configuration inputs have been entered. [Input entered: {data}] [Inputs: {self.configuration_inputs}]")
            if key != None:
                if key not in self.model.config_parameters and validation_req:
                    raise self._raise_exception(
                        f"The key provided [{key}] is not a configuration parameter")

                self.configuration_inputs[key] = data
            else:
                self.configuration_inputs[self.model.config_parameters[self._config_params_entered]] = data
        else:
            raise self._raise_exception(
                "This model does not require configuration data")

        self._config_params_entered += 1

    def show_constraint_stage_not_active_err_msg(self):
        print(
            f"[Constraint {self.name} cannot start. Its stage has not begun]")

    def notify_external_action(self, constraint_name: str, command: str, data: dict) -> Any:
        """This method is run when a model request's input with the external_action(..) method"""

        if self.external_action_func != None:
            return self.external_action_func(constraint_name, command, data, self.external_action_args)
        else:
            raise self._raise_exception(
                f"External action function not set for Constraint [{self.name}].")

    def on_external_action(self, func, *args):
        """Sets the function to be run when notify_external_action(..) method is called"""

        self.external_action_func = func
        self.external_action_args = args

    def on_config_action(self, func, *args):
        """Sets the function to be run when notify_config_change(..) method is called"""

        self.notify_config_action_func = func
        self.notify_config_action_args = args

    def notify_config_change(self, data):
        """This method is called when a value is modified in the self.configuration_inputs dict is modified."""
        if self.notify_config_action_func != None:
            self.notify_config_action_func(
                data, self.notify_config_action_args)

    def show_constraint_already_ran_error_msg(self):
        print(f"[Constraint {self.name} cannot start. It has already run]")

    def set_stage(self, stage):
        self.stage = stage
        self.flag.log.attach(stage)

        # Child constraint's have to be passed the stage object manually
        if self.model.model_family == ModelFamily.COMBINED_CONSTRAINT:
            for constraint in self.inputs:
                constraint.set_stage(stage)

    def _raise_exception(self, exception_msg, extra_info="") -> Exception:
        """Raias"""
        self.inputs.clear()
        self.flag.log_error(exception_msg+extra_info)
        return Exception(exception_msg+extra_info)
