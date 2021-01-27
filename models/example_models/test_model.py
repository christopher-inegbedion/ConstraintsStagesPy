import time

from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model
from enums.constraint_input_mode import ConstraintInputMode


class TestModel(Model):
    def __init__(self):
        self.name = "test"
        self.model_family = ModelFamily.CONSTRAINT
        self.initial_input_required = False
        self.input_type = InputType.INT
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 1
        self.output_type = InputType.INT

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count,
                         self.output_type, initial_input_required=self.initial_input_required,)

    def run(self, inputs: list):
        super().run(inputs)
        self.pause(10)

        input1 = self.request_input()
        self._complete(input1)

    def _complete(self, data, aborted=False):
        super()._complete(data)
