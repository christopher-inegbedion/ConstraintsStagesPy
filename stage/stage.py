from constraints.constraint_main.constraint import Constraint


class Stage:
    """A stage is a collection of constraints"""

    def __init__(self, name: str):
        self.name = name
        self.constraints = []

    def start(self):
        """Begin a stage and its constraints"""
        print(f">>{self.name}<<")

        if len(self.constraints) > 0:
            for constraint in self.constraints:
                constraint.start()
        else:
            raise Exception(
                "Constraints have not been passed to this stage")

    def add_constraint(self, constraint: Constraint):
        """Add a constraint to the stage"""
        if constraint != None or type(constraint) != Constraint:
            self.constraints.append(constraint)
        else:
            raise Exception("An invalid constraint was passed")

    def remove_constraint(self, constraint: Constraint):
        """Remove a constraint from a stage"""
        if len(self.constraints) > 0:
            self.constraints.remove(constraint)
        else:
            raise Exception("Constraints have not been added to the stage")


class StageGroup:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def start(self):
        for stage in self.stages:
            stage.start()
