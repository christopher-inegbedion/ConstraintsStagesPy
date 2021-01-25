from constraint import Constraint
from flag import Flag
from models.example_models.constraint_input_model import ConstraintInputModel


class CombinedConstraintConstraintInput(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("CombinedConstraintConstraintInput", False, 0, 0, False, False, "", "")
        self.model = ConstraintInputModel()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()