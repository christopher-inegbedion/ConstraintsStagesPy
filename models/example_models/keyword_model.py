from enums.constraint_input_mode import ConstraintInputMode
from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model


class KeywordModel(Model):
    """A custom model. Test the provided input against an existing list of predefined keywords"""

    def __init__(self):
        self.name = "Keyword"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.input_type = InputType.STRING
        self.input_mode = ConstraintInputMode.USER
        self.input_count = 3
        self.output_type = InputType.ANY

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        self._complete(inputs)

    def _complete(self, data):
        print(f"\t{self.constraint.name} complete with output -> {data}")
        super()._complete(data)
