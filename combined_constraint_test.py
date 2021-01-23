from constraint import Constraint
from flag import Flag
from models.boolean_model import BooleanModel


class CombinedConstraintTest(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("TestCombinedConstraint", False, 0, 0, False, False, "", "")
        self.model = BooleanModel()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
