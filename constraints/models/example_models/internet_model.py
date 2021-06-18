from constraints.enums.constraint_input_mode import ConstraintInputMode
from constraints.enums.model_family import ModelFamily
from constraints.enums.input_type import InputType
from constraints.models.model_parent import Model
import requests
import jsonpickle


class InternetModel(Model):
    def __init__(self):
        self.name = "InternetModel"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.STRING
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 2
        self.output_type = InputType.STRING
        self.config_parameters = ["test", "test1"]

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type, configuration_input_count=2, configuration_input_required=True, config_parameters = self.config_parameters)

    def run(self, inputs: list, configuration_inputs={}):
        super().run(inputs)

        base_currency = inputs[0]
        target_currency = inputs[1]
        api_key = "c53ef4f33c8f502a2837e646"
        addr = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"

        r = requests.get(addr)
        if r.status_code == 200:
            response = {"response": r.json()}
            print(response["response"]["conversion_rate"])
        else:
            response = {"response": "failure"}
            print("failure")

        self._complete(jsonpickle.encode(response))

    def _complete(self, data, aborted=False):
        super()._complete(data, aborted)
