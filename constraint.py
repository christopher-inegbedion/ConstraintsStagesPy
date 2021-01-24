from flag import Flag
from models.model_parent import Model
from abc import ABC, abstractmethod
from enums.input_type import InputType
from enums.constraint_input_type import ConstraintInputType


class Constraint(ABC):
    """Abstract constraint class"""
    def __init__(self, name: str, flag: Flag, model: Model):
        """Each constraint has a flag and model

        Flag :- The flag defines the properties for the constraint
        Model :- The model defines what the constraint needs (i.e inputs),
                 what it does and what it produces

        Order of operation :- [INPUT]start() -> [MODEL]model.run([INPUT]) -> [OUTPUT]complete(data)"""
        self.name = name
        self.flag = flag
        self.inputs = []
        self.model = model
        self.output = None

    @abstractmethod
    def start(self):
        """This method starts the constraint"""
        self.flag.start_constraint()  # initialize the constraint's flag details.

        if self.model.input_mode == ConstraintInputType.USER:
            for input_count in range(self.model.input_count):
                user_input = input("input: ")
                # validate and add the input provided by the user
                self.validate_and_add_user_input(user_input)
        elif self.model.input_mode == ConstraintInputType.PRE_DEF:
            if len(self.inputs) > self.model.input_count:
                raise Exception("Inputs entered more that required number of inputs")

        # begin the model
        self.model.run(self.inputs)

    def validate_and_add_user_input(self, data):
        """This method validates the data provided by the constraint user. Used for USER input mode."""
        if self.model.input_type == InputType.BOOL:  # boolean input
            if data.lower() == "true":
                self.inputs.append(True)
            elif data.lower() == "false":
                self.inputs.append(False)
            else:
                raise Exception("Invalid constraint input (BOOl type required)")

        elif self.model.input_type == InputType.STRING:  # string input
            self.inputs.append(data)

        elif self.model.input_type == InputType.INT:  # int input
            if type(data) == str:
                if data.isnumeric():
                    self.inputs.append(int(data))
            else:
                raise Exception("Invalid constraint input (INT type required)")

    def validate_and_add_predef_input(self, data):
        """This method validates the data provided by the constraint. Used for PRE_DEF input mode."""
        if self.model.input_type == InputType.BOOL:  # bool input
            if type(data) != bool:
                raise Exception("Invalid constraint input (BOOl type required)")
            else:
                self.inputs.append(data)
        elif self.model.input_type == InputType.STRING:  # string input
            if type(data) != str:
                raise Exception("Invalid constraint input (STRING type required)")
            else:
                self.inputs.append(data)
        elif self.model.input_type == InputType.INT:  # int input
            if type(data) != int:
                raise Exception("Invalid constraint input (INT type required)")
            else:
                self.inputs.append(data)
        elif self.model.input_type == InputType.CONSTRAINT:  # constraint input
            self.inputs.append(data)

    def add_input(self, data):
        """Add input to the constraint. This method is only used if the input mode is PRE_DEF"""
        # verify the input provided
        self.validate_and_add_predef_input(data)



