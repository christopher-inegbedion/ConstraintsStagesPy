import time

from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model
from enums.constraint_input_type import ConstraintInputType


class TestModel(Model):
    def __init__(self):
        self.name = "test"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.BOOL
        self.input_mode = ConstraintInputType.PRE_DEF
        self.input_count = 1
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count,
                         self.output_type)

    def run(self, inputs: list):
        print(f"{self.constraint.name} model running")
        print(f"->{inputs}")
        time.sleep(10)
        self._complete(inputs[0])

    def _complete(self, data):
        print(f"Complete with output -> {data}")
        super()._complete(data)

        # print(f"{self.constraint.name}")
        self.output = data
        self.constraint.output = data
        print()
