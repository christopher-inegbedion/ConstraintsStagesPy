from constraints.enums.constraint_input_mode import ConstraintInputMode
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.models.model_parent import Model
import time


class PauseModel(Model):
    def __init__(self):
        self.name = "PauseModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.INT
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 1
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type)

    def run(self, inputs):
        super().run(inputs)

        time.sleep(inputs[0])

        self._complete(False)

    def _complete(self, data, aborted=False):
        super()._complete(data, aborted)
