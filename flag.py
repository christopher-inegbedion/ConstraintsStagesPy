from enum import Enum
import time


class Flag:
    def __init__(self, name: str, started: bool, start_time: int, end_time: int, required: bool, combined: bool,
                 prev_constraint_id: str,
                 next_constraint_id: str):
        self.name = name
        self.started = started
        self.start_time = start_time
        self.end_time = end_time
        self.required = required
        self.combined = combined
        self.prev_constraint_id = prev_constraint_id
        self.next_constraint_id = next_constraint_id

    def start_constraint(self):
        self.started = True
        self._set_start_time()

    def complete_constraint(self):
        self._set_end_time()

    def _set_start_time(self):
        self.start_time = int(time.time())

    def _set_end_time(self):
        self.end_time = int(time.time())

    def set_required(self, required: bool):
        self.required = required

    def set_combined(self, combined: bool):
        self.combined = combined

    def set_prev_constraint_id(self, prev_constraint_id: str):
        self.prev_constraint_id = prev_constraint_id

    def set_next_constraint_id(self, next_constraint_id: str):
        self.next_constraint_id = next_constraint_id
