import time


class Flag:
    """The flag describes a constraints properties"""
    def __init__(self, name: str, started: bool, start_time: int, end_time: int, required: bool, combined: bool,
                 prev_constraint_id: str,
                 next_constraint_id: str):
        self.name = name  # flag name tag
        self.started = started  # defines if the constraint has begun
        self.start_time = start_time  # a UNIX timestamp from when the constraint begun
        self.end_time = end_time  # a UNIX timestamp from when the constraint completes
        self.required = required  # defines if the constraint is required in a stage. This property is only useful for
        # constraints with a USER input mode
        self.combined = combined  # this value defines if a constraint is combined
        self.prev_constraint_id = prev_constraint_id  # the ID of the previous constraint
        self.next_constraint_id = next_constraint_id  # the ID of the next constraint

    def start_constraint(self):
        """Called when a constraint is begun"""
        self.started = True
        self._set_start_time()

    def complete_constraint(self):
        """Called when a constraint is completed"""
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

    def set_prev_constraint_id(self, prev_constraint_id: str):
        """Set the previous constraint ID. Method used by the stage"""
        self.prev_constraint_id = prev_constraint_id

    def set_next_constraint_id(self, next_constraint_id: str):
        """Set the next constraint ID. Method used by the stage"""
        self.next_constraint_id = next_constraint_id
