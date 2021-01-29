class Stage:
    def __init__(self, name: str):
        self.name = name
        self.constraints = []

    def start(self):
        print(f">>{self.name}<<")
        for constraint in self.constraints:
            constraint.start()

    def add_constraint(self, constraint):
        self.constraints.append(constraint)


class StageGroup:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def start(self):
        for stage in self.stages:
            stage.start()
