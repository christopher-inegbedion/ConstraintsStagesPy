from constraint import Constraint
from flag import Flag
from models.example_models.boolean_model_or import BooleanModelOR


class CombinedConstraintBoolOR(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("CombinedConstraintBoolOR", False, 0, 0, False, False, "", "")
        self.model = BooleanModelOR()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
