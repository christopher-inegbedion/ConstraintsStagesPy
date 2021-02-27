from constraints.models.model_parent import Model
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode


class VerificationModel(Model):
    """A custom model. Verify the input against a keyword list"""

    def __init__(self):
        self.name = "VerificationModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.LIST_AND_STRING
        self.input_mode = ConstraintInputMode.MIXED_USER_PRE_DEF
        self.input_count = 2
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        keywords = inputs[0]
        user_input = inputs[1]

        if user_input in keywords:
            self._complete(True)
        else:
            self._complete(False)

    def _complete(self, data, aborted=False):
        super()._complete(data)
