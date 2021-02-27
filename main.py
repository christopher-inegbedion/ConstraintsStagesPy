from constraints.constraint_main.custom_constraint import CustomConstraint
from constraints.models.example_models.boolean_model_and import BooleanModelAND
from constraints.models.example_models.constraint_input_model import ConstraintInputAsOutputModel
from constraints.models.example_models.keyword_model import KeywordModel
from constraints.models.example_models.test_combined_constraint import TestCombinedConstraintModel
from constraints.models.example_models.test_model import TestModel
from constraints.models.example_models.time_model import TimeModel
from constraints.models.example_models.verification_model import VerificationModel
from stage.stage import Stage, StageGroup

# keyword_model = KeywordModel()
# keyword_model.set_input_count(5)
#
# constraint_input_as_output_model = ConstraintInputAsOutputModel()
# constraint_input_as_output_model.set_input_count(9)
# constraint_input_as_output_model.set_input_count_growable()
#
# test_constraint3 = CustomConstraint("time constraint 1", TimeModel())
# test_constraint4 = CustomConstraint("time constraint 2", TimeModel())
# test_constraint5 = CustomConstraint("time constraint 3", TimeModel())
# test_constraint = CustomConstraint("keyword constraint", keyword_model)
# test_constraint2 = CustomConstraint("verification constraint", VerificationModel())
#
# test_constraint6 = CustomConstraint("constraint-input constraint", constraint_input_as_output_model)
# test_constraint7 = CustomConstraint("time constraint", TimeModel())
#
# test_constraint6.add_input(test_constraint3)
# test_constraint6.add_input(test_constraint4)
# test_constraint6.add_input(test_constraint5)
# test_constraint6.add_input(test_constraint)
# test_constraint6.add_input(test_constraint2)
#
# # test_constraint8 = CustomConstraint("boolean AND constraint", BooleanModelAND())
# # test_constraint8.add_input(test_constraint6)
# # test_constraint8.add_input(test_constraint7)
#
# test_constraint6.start()

# test_constraint_1 = CustomConstraint("test constraint", TestModel())
# test_constraint_1.add_input(False)
# test_constraint_1.start()

constraint1 = CustomConstraint("test1", TestModel())
constraint1.add_input(4)
constraint2 = CustomConstraint("test2", TestModel())

combined_constraint = CustomConstraint(
    "combined constraint", TestCombinedConstraintModel(), debug=True)
combined_constraint.add_input(constraint1)
combined_constraint.add_input(constraint2)

stage = Stage("stage 1")
stage.add_constraint(combined_constraint)

stage2 = Stage("stage 2")
stage2.add_constraint(combined_constraint)

stage_group = StageGroup()
stage_group.add_stage(stage)
stage_group.add_stage(stage2)
stage_group.start()
