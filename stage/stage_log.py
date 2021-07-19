from constraints.enums.stage_status import StageStatus


class StageLog:
    """Record Stage events"""

    def __init__(self):
        self.events = {}
        self.most_recent_update = {}
        self._init()
        self.pipeline = None

    def _init(self):
        for e in StageStatus:
            self.events[e] = None

    def attach(self, observer) -> None:
        self.pipeline = observer

    def detach(self, observer) -> None:
        self.pipeline = observer

    def notify(self):
        if self.pipeline is not None:
            self.pipeline.update(self)

    def update_log(self, event: StageStatus, value, msg):
        if event in self.events:
            self.events[event] = {"value": value, "msg": msg}
            self.most_recent_update.clear()
            self.most_recent_update = {
                "event": event, "value": value, "msg": msg}
            self.notify()
        else:
            raise Exception(f"Stage event type '{event}' cannot be found")
