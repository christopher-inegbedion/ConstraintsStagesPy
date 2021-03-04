from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint
from constraints.models.example_models.boolean_model_and import BooleanModelAND
from constraints.models.example_models.constraint_input_model import ConstraintInputAsOutputModel
from constraints.models.example_models.keyword_model import KeywordModel
from constraints.models.example_models.test_combined_constraint import TestCombinedConstraintModel
from constraints.models.example_models.test_model import TestModel
from constraints.models.example_models.time_model import TimeModel
from constraints.models.example_models.verification_model import VerificationModel
from stage.stage import Stage, StageGroup
import time
import asyncio


constraint1 = CustomConstraint("test1", TestModel(), debug=True)
constraint1.add_input(4)
constraint2 = CustomConstraint("test2", TestModel())
constraint2.add_input(4)
constraint3 = CustomConstraint("test3", TestModel(), debug=True)
constraint3.add_input(4)
constraint4 = CustomConstraint("test4", TestModel())
constraint4.add_input(4)

combined_constraint = CustomConstraint(
    "combined constraint", TestCombinedConstraintModel(), debug=True)
combined_constraint.add_input(constraint1)
combined_constraint.add_input(constraint2)

time_constraint = CustomConstraint(
    "time", PauseModel(), debug=False
)
time_constraint.add_input(20)

stage = Stage("stage 1")
stage.add_constraint(time_constraint)
stage.add_constraint(combined_constraint)

stage2 = Stage("stage 2")
stage2.add_constraint(combined_constraint)
stage2.add_constraint(constraint1)
stage2.add_constraint(constraint3)
# stage2.add_constraint(constraint4)

stage_group = StageGroup()
stage_group.add_stage(stage)
stage_group.add_stage(stage2)
stage_group.start()

stage.start_constraint("time")
# time.sleep(5)
stage.stop_constraint("time")
stage.start_constraint("combined constraint")
