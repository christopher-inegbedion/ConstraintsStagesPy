from constraint import Constraint
from flag import Flag


class CustomConstraint(Constraint):
    """A custom constraint class to create constraints and can be fitted with any model of choice"""

    def __init__(self, name, model, flag=None):
        self.name = name
        self.model = model
        self.flag = Flag("ConstraintVerification", False, 0, 0, False, False, "", "")

        super().__init__(self.name, self.flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
