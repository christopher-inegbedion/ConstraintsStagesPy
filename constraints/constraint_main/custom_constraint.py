from constraints.constraint_main.constraint import Constraint
from constraints.enums.constraint_status import ConstraintStatus
from constraints.constraint_main.flag import Flag


class CustomConstraint(Constraint):
    """A custom constraint class to create constraints that can be fitted with any model of choice.

    This class enables to creation of constraints by just assigning it a name(for debugging) and
     a model of choice to get started"""

    def __init__(self, name, model, flag=None, debug=False):
        super().__init__(name, flag, model, debug)

    def start(self):
        super().start()
