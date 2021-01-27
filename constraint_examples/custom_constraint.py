from constraint import Constraint
from enums.constraint_status import ConstraintStatus
from flag import Flag


class CustomConstraint(Constraint):
    """A custom constraint class to create constraints that can be fitted with any model of choice.

    This class enables to creation of constraints by just assigning it a name(for debugging) and
     a model of choice to get started"""

    def __init__(self, name, model, flag=None):
        self.name = name
        self.model = model

        # support for providing custom flags
        if flag is not None:
            self.flag = flag
        else:
            self.flag = Flag("ConstraintVerification", ConstraintStatus.NOT_STARTED, False, False, False, "", "")

        super().__init__(self.name, self.flag, self.model)
        self.model.set_constraint(self)

    def start(self):
        super().start()
