from constraint_examples.custom_constraint import CustomConstraint
from models.example_models.boolean_model_and import BooleanModelAND
from models.example_models.constraint_input_model import ConstraintInputModel
from models.example_models.keyword_model import KeywordModel
from models.example_models.time_model import TimeModel
from models.example_models.verification_model import VerificationModel

test_constraint = CustomConstraint("keyword constraint", KeywordModel())
test_constraint2 = CustomConstraint("verification constraint", VerificationModel())
test_constraint3 = CustomConstraint("constraint-input constraint", ConstraintInputModel())
test_constraint4 = CustomConstraint("time constraint", TimeModel())

test_constraint3.add_input(test_constraint)
test_constraint3.add_input(test_constraint2)

test_constraint5 = CustomConstraint("boolean AND constraint", BooleanModelAND())
test_constraint5.add_input(test_constraint4)
test_constraint5.add_input(test_constraint3)

test_constraint5.start()

