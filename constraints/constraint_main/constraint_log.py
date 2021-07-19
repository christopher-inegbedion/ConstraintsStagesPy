from constraints.enums.constraint_status import ConstraintStatus
from utils.update import Observable


class ConstraintLog(Observable):
    """Record constraint events"""

    def __init__(self):
        self.events = {}
        self.most_recent_update = {}
        self._init()
        self.stage = None

    def _init(self):
        for e in ConstraintStatus:
            self.events[e] = None

    def attach(self, observer) -> None:
        self.stage = observer

    def detach(self, observer) -> None:
        self.stage = observer

    def notify(self):
        if self.stage is not None:
            self.stage.on_update(self)

    def update_log(self, event: ConstraintStatus, value, msg):
        if event in self.events:
            self.events[event] = {"value": value, "msg": msg}
            self.most_recent_update.clear()
            self.most_recent_update[event] = {"value": value, "msg": msg}
            self.notify()
        else:
            raise Exception(f"Constraint event type '{event}' cannot be found")
