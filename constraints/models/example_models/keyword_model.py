from constraints.constraint_main.constraint import Constraint
from constraints.models.model_parent import Model
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode


class KeywordModel(Model):
    """A custom model. Test the provided input against an existing list of predefined keywords"""

    def __init__(self):
        self.name = "Keyword"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.STRING
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 1
        self.output_type = InputType.ANY
        self.config_parameters = ["passcode"]

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type,
                         configuration_input_count=1, configuration_input_required=True,
                         config_parameters=self.config_parameters)

    def run(self, inputs: list, configuration_inputs={}):
        super().run(inputs)
        value = inputs[0]
        constraint: Constraint = self.constraint

        self.external_action(True, "12", "qw", {})
        requested_input1 = self.external_action(True, "12", "qw", {})
        requested_input2 = self.external_action(True, "2", "", {})
        # print(int(requested_input1)*int(requested_input2))

        self._complete(inputs)

    def _complete(self, data, aborted=False):
        super()._complete(data)
