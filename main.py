from constraint_examples.custom_constraint import CustomConstraint
from models.example_models.boolean_model_and import BooleanModelAND
from models.example_models.constraint_input_model import ConstraintInputAsOutputModel
from models.example_models.keyword_model import KeywordModel
from models.example_models.time_model import TimeModel
from models.example_models.verification_model import VerificationModel

keyword_model = KeywordModel()
# keyword_model.set_input_count(5)

constraint_input_as_output_model = ConstraintInputAsOutputModel()
constraint_input_as_output_model.set_input_count(9)
constraint_input_as_output_model.set_input_count_growable()

test_constraint3 = CustomConstraint("time constraint 1", TimeModel())
test_constraint4 = CustomConstraint("time constraint 2", TimeModel())
test_constraint5 = CustomConstraint("time constraint 3", TimeModel())
test_constraint = CustomConstraint("keyword constraint", keyword_model)
test_constraint2 = CustomConstraint("verification constraint", VerificationModel())

test_constraint6 = CustomConstraint("constraint-input constraint", constraint_input_as_output_model)
test_constraint7 = CustomConstraint("time constraint", TimeModel())

test_constraint6.add_input(test_constraint3)
test_constraint6.add_input(test_constraint4)
test_constraint6.add_input(test_constraint5)
test_constraint6.add_input(test_constraint)
test_constraint6.add_input(test_constraint2)

# test_constraint8 = CustomConstraint("boolean AND constraint", BooleanModelAND())
# test_constraint8.add_input(test_constraint6)
# test_constraint8.add_input(test_constraint7)

test_constraint6.start()
