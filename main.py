from constraint_examples.custom_constraint import CustomConstraint
from models.example_models.constraint_input_model import ConstraintInputModel
from models.example_models.keyword_model import KeywordModel
from models.example_models.verification_model import VerificationModel

test_constraint = CustomConstraint("keyword constraint", KeywordModel())
test_constraint2 = CustomConstraint("verification constraint", VerificationModel())
test_constraint3 = CustomConstraint("constraint-input constraint", ConstraintInputModel())

test_constraint3.add_input(test_constraint)
test_constraint3.add_input(test_constraint2)

test_constraint3.start()

