import logging
import time

from constraints.constraint_main.constraint_log import ConstraintLog
from constraints.enums.constraint_status import ConstraintStatus


class Flag:
    """The flag describes a constraints properties"""

    def __init__(self, name: str, status: ConstraintStatus, initial_input_required: bool, required: bool, combined: bool,
                 prev_constraint_id: str,
                 next_constraint_id: str):
        self.name = name  # flag name tag

        # defines the status of the constraint (Active, Complete, etc)
        self.status = status

        # a UNIX timestamp from when the constraint begun
        self.start_time = 0

        # a UNIX timestamp from when the constraint completes
        self.end_time = 0

        # Defines if the constraint is required in a stage. This property is only useful for
        # constraints with a USER input mode
        self.required = required

        # this value defines if a constraint is combined
        self.combined = combined

        # Defines if initial input is required. If this field's value is true, then the input count
        # value for the constraint's model is ignored and the input is entered on request of the model
        self.initial_input_required = initial_input_required

        # the ID of the previous constraint
        self.prev_constraint_id = prev_constraint_id

        # the ID of the next constraint
        self.next_constraint_id = next_constraint_id

        # tracks the constraint's events
        self._init_log()

        # flag's constraint owner object
        self.constraint = None

    def _init_log(self):
        self.log: ConstraintLog = ConstraintLog()

    def set_constraint(self, constraint):
        self.constraint = constraint

    def log_error(self, err_msg):
        self.set_status(ConstraintStatus.ERROR, None, custom_msg=err_msg)

    def set_status(self, status: ConstraintStatus, data, custom_msg: str = ""):
        """Sets the constraints status"""
        logging.basicConfig(level=logging.DEBUG)

        self.status = status
        if status == ConstraintStatus.ACTIVE:
            msg = f"Constraint [{self.constraint.name}] has started"
            self.log.update_log(self.status, True,
                                msg)
            self._set_start_time()

        elif status == ConstraintStatus.INPUT_PASSED:
            msg = f"Constraint [{self.constraint.name}] has value [{data}] inputted."
            self.log.update_log(self.status, data,
                                msg)

        elif status == ConstraintStatus.PENDING_INPUT:
            msg = f"Constraint [{self.constraint.name}] with model [{self.constraint.model.name}] has requested input."
            self.log.update_log(
                self.status, True,
                msg)

        elif status == ConstraintStatus.PAUSED:
            msg = f"Constraint [{self.constraint.name}] with model [{self.constraint.model.name}] has been paused."
            self.log.update_log(
                self.status, data, msg
            )

        elif status == ConstraintStatus.RESUMED:
            msg = f"Constraint [{self.constraint.name}] has resumed"
            self.log.update_log(
                self.status, True, msg)

        elif status == ConstraintStatus.COMPLETE:
            msg = f"Constraint [{self.constraint.name}] has completed"
            self.log.update_log(self.status, True,
                                msg)
            self._set_end_time()

        elif status == ConstraintStatus.OUTPUT_PRODUCED:
            msg = f"Constraint [{self.constraint.name}] completed with value {data}"
            self.log.update_log(self.status, data,
                                msg)

        elif status == ConstraintStatus.ERROR:
            msg = f"Constraint [{self.constraint.name}] encounterd an error"
            if custom_msg != "":
                msg = custom_msg
            self.log.update_log(self.status, data, msg)
        else:
            msg = f"ConstraintStatus [{status}] has not been implemented"
            self.log.update_log(ConstraintStatus.ERROR, None, msg)

        self._display_debug_info(msg)

    def _display_debug_info(self, msg):
        if self.constraint.debug:
            logging.debug(msg)

    def start_constraint(self, input):
        """Called when a constraint is begun"""
        self.set_status(ConstraintStatus.ACTIVE, input)

    def complete_constraint(self, output):
        """Called when a constraint is completed"""
        self.set_status(ConstraintStatus.COMPLETE, output)

    def _set_start_time(self):
        """Set the UNIX timestamp for when the constraint begun"""
        self.start_time = int(time.time())

    def _set_end_time(self):
        """Set the UNIX timestamp for when the constraint completes"""
        self.end_time = int(time.time())

    def set_required(self, required: bool):
        """Set the constraint as required in a stage. Method used by the constraint"""
        self.required = required

    def set_combined(self, combined: bool):
        """Set the constraint as combined. Method used by the model"""
        self.combined = combined

    def set_initial_input_required(self, required: bool):
        """Set whether or not initial input is required"""

    def set_prev_constraint_id(self, prev_constraint_id: str):
        """Set the previous constraint ID. Method used by the stage"""
        self.prev_constraint_id = prev_constraint_id

    def set_next_constraint_id(self, next_constraint_id: str):
        """Set the next constraint ID. Method used by the stage"""
        self.next_constraint_id = next_constraint_id
