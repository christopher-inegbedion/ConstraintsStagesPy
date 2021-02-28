from typing import List
from constraints.constraint_main.constraint import Constraint


class Stage:
    """A collection of constraints"""

    def __init__(self, name: str):
        self.name = name
        self.constraints: List[Constraint] = []

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

    def freeze(self):
        """Pause the stage, and any running constraints"""
        for constraint in self.constraints:
            constraint.pause()


class StageGroup:
    """A group of stages"""

    def __init__(self):
        self.stages: List[Stage] = []
        self.status = None

    def _get_stage_with_name(self, stage_name: str) -> Stage:
        for stage in self.stages:
            if stage.name == stage_name:
                return stage

        return None

    def add_stage(self, stage: Stage):
        """Add a stage"""
        self.stages.append(stage)

    def remove_stage(self, stage_name: str):
        """Remove a stage provided its name"""
        if len(self.stages) > 0:
            self.stages.remove(self._get_stage_with_name(stage_name))
        else:
            raise Exception("There are no stages in the stage group")

    def start(self, stage_name=""):
        """Start a stage given its name"""
        if stage_name == "":
            if len(self.stages) > 0:
                for stage in self.stages:
                    stage.start()
            else:
                raise Exception("There are no stages in the stage group")
        else:
            if len(self.stages) > 0:
                stage = self._get_stage_with_name(stage_name)
                if stage != None:
                    stage.start()
                else:
                    raise Exception(f"The stage:'{stage_name}' does not exist")
            else:
                raise Exception("There are no stages in the stage group")
