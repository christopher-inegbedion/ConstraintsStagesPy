from enums.constraint_input_mode import ConstraintInputMode
from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model
import arrow


class TimeModel(Model):
    """A custom model. Waits for the time set by the user."""
    def __init__(self):
        self.name = "TimeModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.INT
        self.input_mode = ConstraintInputMode.USER
        self.input_count = 1
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        time_ahead_from_input = inputs[0]

        current_time = arrow.now()
        time_ahead = current_time.shift(seconds=time_ahead_from_input).format("ss")

        while arrow.now().format("ss") != time_ahead:
            print(f"waiting...")

        self._complete(True)

    def _complete(self, data, aborted=False):
        super()._complete(data)


