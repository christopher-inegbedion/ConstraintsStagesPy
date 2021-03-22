from stage.stage_log import StageLog
from constraints.constraint_main.constraint_log import ConstraintLog
import constraints
from constraints.enums.constraint_status import ConstraintStatus
from constraints.enums.stage_status import StageStatus
from typing import List
import threading
from constraints.constraint_main.constraint import Constraint
import concurrent.futures
import time
from utils.update import Observable, Observer
from constraints.constraint_main.flag import Flag


class Stage(Observer):
    """A collection of constraints"""

    def __init__(self, name: str, display_log=False):
        self.name = name
        self.constraints: List[Constraint] = []
        self.stage_group: StageGroup = None
        self.status: StageStatus = StageStatus.NOT_STARTED
        self.has_constraint_started = False
        self.log = StageLog()
        self.pipeline = None
        self._display_log = display_log

        # The current constraint running
        self.running_constraints: List[Constraint] = []

    def on_update(self, observer: ConstraintLog) -> None:
        """Notifies the Stage of a change in the Constraint"""
        if self._display_log:
            print(observer.most_recent_update)

    def start(self):
        """Create a new thread for the stage"""
        threading.Thread(target=self._start, args=()).start()

    def _start(self):
        """Main function to begin a stage"""
        if self.stage_group == None:
            raise Exception("A stage group does not exist")

        with self.stage_group.stage_thread_instance_lock:
            print(f">>{self.name} stage STARTED")
            self.log.update_log(
                "STAGE_STARTED", True, f"Stage {self.name} has STARTED")

            if len(self.constraints) > 0:
                self.stage_group.set_current_stage(self)
            else:
                raise Exception(
                    "Constraints have not been passed to this stage")

            while self.status != StageStatus.COMPLETE:
                if len(self.running_constraints) > 0:
                    are_all_constraints_complete = True
                    for constraint in self.constraints:
                        if constraint.get_status() != ConstraintStatus.COMPLETE:
                            are_all_constraints_complete = False

                    if are_all_constraints_complete:
                        self._complete()

    def _complete(self):
        """Complete the stage"""
        print(f">>{self.name} stage COMPLETE")
        self.running_constraints.clear()
        self.log.update_log(
            "STAGE_COMPLETED", True, f"Stage {self.name} has COMPLETED")

        self.status = StageStatus.COMPLETE

    def set_task_for_constraint(self, constraint_name, task):
        constraint = self.get_constraint(constraint_name)
        constraint.set_task_instance(task)

    def get_constraint(self, name):
        """Find a constraint in the stage"""
        for cnstrt in self.constraints:
            if cnstrt.name == name:
                return cnstrt

        raise Exception("Constraint cannot be found")

    def start_constraint(self, name, debug=False):
        """Start a new thread for a constraint"""
        constraint = self.get_constraint(name)

        # this pause in the main thread is need to give time for the stage to begin
        time.sleep(0.25)

        # Start a constraint only if the stage is running
        if self.status == StageStatus.ACTIVE:
            self.running_constraints.append(constraint)

            new_constraint = threading.Thread(
                target=constraint.start, args=())
            new_constraint.setName(constraint.name)

            new_constraint.start()
        else:
            constraint.show_constraint_stage_not_active_err_msg()

    def stop(self):
        """Stop a constraint"""
        is_there_no_active_constraint = True

        for constraint in self.constraints:
            if constraint.get_status() == ConstraintStatus.ACTIVE:
                is_there_no_active_constraint = False
                self.stop_constraint(constraint.name)

        print(f">Stage: {self.name} is stopped.")

        if is_there_no_active_constraint:
            self._complete()

    def upgrade_status(self):
        if self.has_constraint_started is False:
            if self.status == StageStatus.NOT_STARTED:
                self.status = StageStatus.ACTIVE
            self.has_constraint_started = True

    def set_stage_group(self, stage_group):
        self.stage_group = stage_group

    def add_constraint(self, constraint):
        """Add a constraint to the stage"""
        if constraint != None:
            self.constraints.append(constraint)
            constraint.set_stage(self)
        else:
            raise Exception("An invalid constraint was passed")

    def remove_constraint(self, constraint):
        """Remove a constraint from a stage"""
        if len(self.constraints) > 0:
            self.constraints.remove(constraint)
        else:
            raise Exception("Constraints have not been added to the stage")

    def stop_constraint(self, constraint_name):
        """Stop a constraint"""
        self.get_constraint(constraint_name).model.abort()

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline
        self.log.attach(pipeline)


class StageGroup:
    """A group of stages"""

    def __init__(self):
        self.stages: List[Stage] = []
        self.status = None
        self.current_stage = "None"

        self.stage_threads = []

        # allows for a single stage to be active at any time
        self.stage_thread_instance_lock = threading.Lock()

    def set_current_stage(self, current_stage: Stage):
        self.current_stage = current_stage
        current_stage.upgrade_status()

    def _get_stage_with_name(self, stage_name: str) -> Stage:
        for stage in self.stages:
            if stage.name == stage_name:
                return stage

        raise Exception("Stage cannot be found")

    def add_stage(self, stage: Stage):
        """Add a stage"""
        self.stages.append(stage)
        stage.set_stage_group(self)

    def remove_stage(self, stage_name: str):
        """Remove a stage provided its name"""
        self.stages.remove(self._get_stage_with_name(stage_name))

    def start(self, stage_name=""):
        """Start a stage given its name"""

        if stage_name == "":
            if len(self.stages) > 0:
                # TODO: Make the start function for the Stages async so they launch when the previous stage is complete.
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

    def set_task_for_constraint(self, constraint_name, task):
        constraint = self.get_constraint(constraint_name)
        constraint.set_task_instance(task)

    def set_task_for_stage(self, stage_name, task):
        stage = self._get_stage_with_name(stage_name)
        for constraint in stage.constraints:
            stage.set_task_for_constraint(constraint.name, task)

    def stop_stage(self, stage_name):
        stage = self._get_stage_with_name(stage_name)
        stage.stop()

    def stop_all(self):
        for stage in self.stages:
            stage.stop()
