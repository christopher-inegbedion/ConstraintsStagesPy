from enums.constraint_input_mode import ConstraintInputType
from enums.input_type import InputType
from enums.model_family import ModelFamily
from models.model_parent import Model


class ConstraintInputModel(Model):
    """A custom model. A model for combined constraints that pass their outputs
    as input to the next constraint, excluding the first constraint"""

    def __init__(self):
        self.name = "ConstraintInputModel"
        self.model_family = ModelFamily.COMBINED_CONSTRAINT
        self.input_type = InputType.CONSTRAINT
        self.input_mode = ConstraintInputType.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.ANY

        super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)

        print(f"{self.constraint.name} model running")

        # get each constraint
        constraint1 = inputs[0]
        constraint2 = inputs[1]
        # constraint3 = inputs[2]

        constraint1.start()
        value1 = constraint1.output
        constraint2.add_input(value1)
        constraint2.start()
        value2 = constraint2.output
        # constraint3.add_input(value2)
        # constraint3.start()
        # value3 = constraint3.output

        self._complete(value2)

    def _complete(self, data):
        print(f"\t{self.constraint.name} complete with output -> {data}")
        super()._complete(data)

