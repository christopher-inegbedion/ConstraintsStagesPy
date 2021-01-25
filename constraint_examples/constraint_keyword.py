from constraint import Constraint
from flag import Flag
from models.example_models.keyword_model import KeywordModel


class ConstraintKeyword(Constraint):
    def __init__(self, name):
        self.default_flag = Flag("ConstraintKeyword", False, 0, 0, False, False, "", "")
        self.model = KeywordModel()

        super().__init__(name, self.default_flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()