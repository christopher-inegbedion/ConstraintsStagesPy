from constraint_test import ConstrainTest
from combined_constraint_test import CombinedConstraintTest


test_constraint = ConstrainTest("constraint1")
test_constraint2 = ConstrainTest("constraint2")
test_constraint3 = ConstrainTest("constraint3")

test_combined_constraint = CombinedConstraintTest("combined constraint")
test_combined_constraint2 = CombinedConstraintTest("combined constraint 2")

test_constraint.add_input(True)
test_constraint2.add_input(True)
test_constraint3.add_input(False)

test_combined_constraint.add_input(test_constraint)
test_combined_constraint.add_input(test_constraint2)

test_combined_constraint2.add_input(test_combined_constraint)
test_combined_constraint2.add_input(test_constraint3)
test_combined_constraint2.start()

