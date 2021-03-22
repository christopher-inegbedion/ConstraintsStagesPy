from utils.update import Observable
from constraints.enums.constraint_events import *


class ConstraintLog(Observable):
    """Record constraint events"""

    def __init__(self):
        self.events = {}
        self.most_recent_update = {}
        self._init()
        self.stage = None

    def _init(self):
        for e in ConstraintEvents:
            self.events[e.name] = None

    def attach(self, observer) -> None:
        self.stage = observer

    def detach(self, observer) -> None:
        self.stage = observer

    def notify(self):
        if self.stage is not None:
            self.stage.on_update(self)

    def update_log(self, event, value, msg):
        if event in self.events:
            self.events[event] = {"value": value, "msg": msg}
            self.most_recent_update.clear()
            self.most_recent_update[event] = {"value": value, "msg": msg}
            self.notify()
        else:
            raise Exception(f"Constraint event type '{event}' cannot be found")
