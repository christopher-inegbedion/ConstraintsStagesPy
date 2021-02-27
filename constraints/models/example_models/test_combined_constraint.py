import time

from constraints.models.model_parent import Model
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode


class TestCombinedConstraintModel(Model):
    def __init__(self):
        self.name = "test"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.initial_input_required = False
        self.input_type = InputType.CONSTRAINT
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.INT

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count,
                         self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        constraint1 = inputs[0]
        constraint1.start()
        output1 = constraint1.output

        constraint2 = inputs[1]
        constraint2.add_input(output1)
        constraint2.start()
        output2 = constraint2.output
        self._complete(output2)

    def _complete(self, data, aborted=False):
        super()._complete(data)
