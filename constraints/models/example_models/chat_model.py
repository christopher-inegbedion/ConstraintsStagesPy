from constraints.constraint_main.constraint import Constraint
from constraints.enums.constraint_input_mode import ConstraintInputMode
from constraints.enums.input_type import InputType
from constraints.enums.model_family import ModelFamily
from constraints.models.model_parent import Model


class ChatModel(Model):
    def __init__(self):
        self.name = "ChatModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.STRING
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.ANY

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type, admin_session_independent=False)

    def run(self, inputs: list, configuration_inputs={}):
        super().run(inputs)
        constraint: Constraint = self.constraint
        self._set_configuration_input_value("active", True)
        self._set_configuration_input_value("user_msg", [])
        self._set_configuration_input_value("admin_msg", [])

        while self._get_configuration_input_value("active"):
            print("user")
            self._get_configuration_input_value("user_msg").append(self.external_action(
                True, "ChatModel", "command", {}))
            print(
                f'user msg: {self._get_configuration_input_value("user_msg")}')
            print(
                f'admin msg: {self._get_configuration_input_value("admin_msg")}')

        self._complete(2)

    def run_admin(self):
        super().run_admin()
        constraint: Constraint = self.constraint

        while self._get_configuration_input_value("active"):
            print("admin")
            self._get_configuration_input_value("admin_msg").append(self.external_action(
                True, "ChatModel", "command", {}))
            print(
                f'user msg: {self._get_configuration_input_value("user_msg")}')
            print(
                f'admin msg: {self._get_configuration_input_value("admin_msg")}')

    def listen(self, msg, data):
        if msg == "user":
            self._set_configuration_input_value("user_data", data)
            print(self._get_configuration_input_value("user_data"))
        elif msg == "admin":
            self._set_configuration_input_value("admin_data", data)
            print(self._get_configuration_input_value("admin_data"))

        super().listen(msg, data)

    def _complete(self, data, aborted=False):
        super()._complete(data, aborted)
