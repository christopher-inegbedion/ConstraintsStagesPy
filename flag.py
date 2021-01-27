import time
from enums.constraint_status import ConstraintStatus


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

    def start_constraint(self):
        """Called when a constraint is begun"""
        self.status = ConstraintStatus.ACTIVE
        self._set_start_time()

    def complete_constraint(self):
        """Called when a constraint is completed"""
        self.status = ConstraintStatus.COMPLETE
        self._set_end_time()

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
