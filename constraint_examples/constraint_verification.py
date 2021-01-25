from constraint import Constraint
from flag import Flag
from models.example_models.verification_model import VerificationModel


class ConstraintVerification(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("ConstraintVerification", False, 0, 0, False, False, "", "")
        self.model = VerificationModel()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
