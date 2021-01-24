from constraint import Constraint
from flag import Flag
from models.example_models.test_model import TestModel


class ConstrainTest(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("TestConstraint", False, 0, 0, False, False, "", "")
        self.model = TestModel()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
