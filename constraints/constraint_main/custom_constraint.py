from constraints.constraint_main.constraint import Constraint
from constraints.enums.constraint_status import ConstraintStatus
from constraints.constraint_main.flag import Flag


class CustomConstraint(Constraint):
    """A custom constraint class to create constraints that can be fitted with any model of choice.

    This class enables to creation of constraints by just assigning it a name(for debugging) and
     a model of choice to get started"""

    def __init__(self, name, description, model, is_admin_input_required, flag=None, debug=False, completion_data_labels=[]):
        super().__init__(name, description, flag, model,
                         is_admin_input_required, debug, completion_data_labels)

    def start(self, d=False):
        super().start(d=self.debug)
