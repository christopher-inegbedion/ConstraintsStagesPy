from constraints.models.model_parent import Model
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode


class KeywordModel(Model):
    """A custom model. Test the provided input against an existing list of predefined keywords"""

    def __init__(self):
        self.name = "Keyword"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.input_type = InputType.STRING
        self.input_mode = ConstraintInputMode.USER
        self.input_count = 3
        self.output_type = InputType.ANY

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list, configuration_inputs={}):
        super().run(inputs)

        self._complete(inputs)

    def _complete(self, data, aborted=False):
        super()._complete(data)
