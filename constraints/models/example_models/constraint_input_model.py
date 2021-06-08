from constraints.models.model_parent import Model
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.enums.constraint_input_mode import ConstraintInputMode


class ConstraintInputAsOutputModel(Model):
    """A custom model. A model for combined constraints that pass their outputs
    as input to the next constraint, excluding the first constraint"""

    def __init__(self):
        self.name = "ConstraintInputModel"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.input_type = InputType.CONSTRAINT
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.ANY

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list, configuration_inputs={}):
        super().run(inputs)

        # get each constraint
        constraint1 = inputs[0]
        constraint1.start()
        prev_constraint_val = constraint1.output

        for i in range(1, self.input_count):
            constraint = inputs[i]
            if constraint.model.input_mode == ConstraintInputMode.USER:
                constraint.start()
            else:
                constraint.add_input(prev_constraint_val)
                constraint.start()
            prev_constraint_val = constraint.output

        self._complete(prev_constraint_val)

    def _complete(self, data, aborted=False):
        super()._complete(data)
