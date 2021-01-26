from models.model_parent import Model
from enums.model_family import ModelFamily
from enums.input_type import InputType
from enums.constraint_input_mode import ConstraintInputMode
import time


class BooleanModelAND(Model):
    """A custom model"""

    def __init__(self) -> None:
        self.name = "BooleanAND"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.input_type = InputType.CONSTRAINT
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)
        constraint1 = inputs[0]
        constraint2 = inputs[1]

        constraint1.start()
        value1 = constraint1.output
        constraint2.start()
        value2 = constraint2.output

        return_val = value1 and value2

        self._complete(return_val)

    def _complete(self, data, aborted=False):
        super()._complete(data)

