from constraint_examples.combined_constraint_constraint_input import CombinedConstraintConstraintInput
from constraint_examples.constraint_keyword import ConstraintKeyword
from constraint_examples.constraint_test import ConstrainTest
from constraint_examples.combined_constraint_bool_and import CombinedConstraintBoolAND
from constraint_examples.combined_constraint_bool_or import CombinedConstraintBoolOR
from constraint_examples.constraint_time import ConstraintTime
from constraint_examples.constraint_verification import ConstraintVerification

test_constraint = ConstraintKeyword("constraint1")
test_constraint2 = ConstraintVerification("constraint2")
test_constraint3 = CombinedConstraintConstraintInput("constraint3")

test_constraint3.add_input(test_constraint)
test_constraint3.add_input(test_constraint2)
#
# test_combined_constraint = CombinedConstraintBoolAND("combined constraint 1")
# test_combined_constraint2 = CombinedConstraintBoolOR("combined constraint 2")
#
# test_constraint.add_input()
# test_constraint2.add_input(True)
# test_constraint3.add_input(False)
#
# test_combined_constraint.add_input(test_constraint)
# test_combined_constraint.add_input(test_constraint2)
#
# test_combined_constraint2.add_input(test_combined_constraint)
# test_combined_constraint2.add_input(test_constraint3)
test_constraint3.start()

