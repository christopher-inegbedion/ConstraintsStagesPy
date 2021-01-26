from enums.constraint_input_mode import ConstraintInputMode
from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model


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

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        print(f"{self.constraint.name} model running")

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

    def _complete(self, data):
        print(f"\t{self.constraint.name} complete with output -> {data}")
        super()._complete(data)

