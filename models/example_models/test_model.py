import time

from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model
from enums.constraint_input_mode import ConstraintInputMode


class TestModel(Model):
    def __init__(self):
        self.name = "test"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.BOOL
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 1
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count,
                         self.output_type)

    def run(self, inputs: list):
        super().run(inputs)
        self.abort()
        self._complete(inputs[0])

    def _complete(self, data, aborted=False):
        super()._complete(data)
