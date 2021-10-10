import logging
from os import stat
from constraints.enums.stage_group_status import StageGroupEnum
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
import uuid


class Stage(Observer):
    """A collection of constraints"""

    def __init__(self, name: str, display_log=False):
        # The name of the stage
        self.name = name

        # The constraints in the stage
        self.constraints: List[Constraint] = []

        # The stage's StageGroup
        self.stage_group: StageGroup = None

        # The status of the Stage
        self.status: StageStatus = StageStatus.NOT_STARTED

        # A value that determines if the stage has started
        self.has_stage_started = False

        # A log that keeps track of the stage's events
        self.log = StageLog()

        # The stage's Pipeline
        self.pipeline = None

        # Determines if the log should be displayed in the terminal
        self._display_log = display_log

        # The current constraint running
        self.running_constraints: List[Constraint] = []

    def on_update(self, observer: ConstraintLog) -> None:
        """Notifies the Stage of a change in the Constraint"""
        # if self._display_log:
        #     print(observer.most_recent_update)
        pass

    def start(self):
        """Create a new thread for the stage"""
        threading.Thread(target=self._start, args=()).start()

    def _start(self):
        """Main function to begin a stage"""
        if self.stage_group == None:
            raise Exception("A stage group does not exist")

        # This prevents more than 1 stage in a Stage group from starting
        with self.stage_group.stage_thread_instance_lock:
            if self._display_log:
                print(f">>{self.name} stage STARTED")

            if self.pipeline != None:
                self.pipeline.current_stage = self

            self.set_status(StageStatus.ACTIVE, self.name)

            if len(self.constraints) > 0:
                self.stage_group.set_current_stage(self)
            else:
                self.set_status(
                    StageStatus.ERROR, "Constraints have not been passed to this stage")

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
        if self._display_log:
            print(f">>{self.name} stage COMPLETE")
        self.running_constraints.clear()
        self.stage_group.stage_complete(self.name)
        self.set_status(StageStatus.COMPLETE, self.name)

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
        """Start a new constraint.

        Each constraint runs in a seperate thread. This enables multiple constraints to be run at
        the same time."""
        constraint = self.get_constraint(name)

        # this pause in the main thread is need to give time for the stage to begin
        time.sleep(0.25)

        # Start a constraint only if the stage is running
        if self.status != StageStatus.NOT_STARTED and self.status != StageStatus.COMPLETE:
            if constraint not in self.running_constraints:
                self.running_constraints.append(constraint)

                new_constraint = threading.Thread(
                    name=constraint.name,
                    target=constraint.start, args=())

                new_constraint.start()
            else:
                constraint.show_constraint_already_ran_error_msg()
        else:
            constraint.show_constraint_stage_not_active_err_msg()

    def stop(self):
        """Stop the stage and any active constraints"""

        for constraint in self.constraints:
            if constraint.get_status() == ConstraintStatus.ACTIVE:
                self.stop_constraint(constraint.name)

        print(f">Stage: {self.name} is stopped.")

        self._complete()

    def set_status(self, status: StageStatus, data):
        """Set the status of the Stage"""

        self.status = status
        # This status indicates that the Stage is active
        if status == StageStatus.ACTIVE:
            msg = f"Stage [{self.name}] has started"
            self.has_stage_started = True

        # All constraint's in the Stage has completed running
        elif status == StageStatus.COMPLETE:
            msg = f"Stage [{self.name}] has completed"

        # A constraint just begun
        elif status == StageStatus.CONSTRAINT_STARTED:
            msg = f"Stage [{self.name}]'s constraint [{data}] has started"

        # A constraint just completed
        elif status == StageStatus.CONSTRAINT_COMPLETED:
            msg = f"Stage [{self.name}]'s constraint [{data}] has completed"

        # An error occured
        elif status == StageStatus.ERROR:
            msg = data
        else:
            msg = f"StageStatus [{status}] has not been implemented"
            status = StageStatus.ERROR

        self.log.update_log(status, data, msg)
        self._display_log_msg(msg)

    def _display_log_msg(self, msg):
        """Display the log message"""
        if self._display_log:
            print(msg)

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
    """A StageGroup is a collection of Stages that can be commanded by the StageGroup to perform a command"""

    def __init__(self):
        self.id = uuid.uuid4()
        self.stages: List[Stage] = []
        self.status = StageGroupEnum.NOT_STARTED
        self.current_stage = "None"

        # allows for a single stage to be active at any time
        self.stage_thread_instance_lock = threading.Lock()

    def set_current_stage(self, current_stage: Stage):
        self.current_stage = current_stage

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

        self.status = StageGroupEnum.RUNNING
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

    def stage_complete(self, stage_name):
        stage = self._get_stage_with_name(stage_name)
        for i in range(len(self.stages)):
            if self.stages[i].name == stage.name and i == len(self.stages)-1:
                self.status = StageGroupEnum.COMPLETE

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

    def get_stage_group_details(self):
        details = []
        for stage in self.stages:
            if stage.status == StageStatus.COMPLETE:
                stage_data = {"stage_name": stage.name,
                              "status": "complete", "constraint_data": []}
                for con in stage.constraints:
                    stage_data["constraint_data"].append(
                        {"constraint_name": con.name, "data": con.completion_data})
                details.append(stage_data)
            elif stage.status == StageStatus.ACTIVE:
                stage_data = {"stage_name": stage.name,
                              "status": "active", "constraint_data": []}
                details.append(stage_data)
            elif stage.status == StageStatus.NOT_STARTED:
                stage_data = {"stage_name": stage.name,
                              "status": "not_started", "constraint_data": []}
        return details

    def get_first_constraint_name(self):
        first_stage: Stage = self.stages[0]
        first_constraint: Constraint = first_stage.constraints[0]
        
        return first_constraint.name