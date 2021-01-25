from enums.constraint_input_mode import ConstraintInputType
from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model


class VerificationModel(Model):
    """A custom model. Verify the input against a keyword list"""

    def __init__(self):
        self.name = "VerificationModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.ANY
        self.input_mode = ConstraintInputType.MIXED_USER_PRE_DEF
        self.input_count = 2
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        print(f"{self.constraint.name} model running")

        keywords = inputs[0]
        user_input = inputs[1]


        if user_input in keywords:
            self._complete(True)
        else:
            self._complete(False)

    def _complete(self, data):
        print(f"\t{self.constraint.name} complete with output -> {data}")
        super()._complete(data)
