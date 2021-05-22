from constraints.models.example_models.internet_model import InternetModel
from constraints.models.example_models.test_model import TestModel
from stage.stage import Stage, StageGroup
from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint

cons = CustomConstraint("con", "desc", InternetModel())
cons1 = CustomConstraint("con2", "desc", TestModel())
cons.add_input("EUR")
cons.add_input("USD")
cons1.add_input(1)

s = Stage('s')
s.add_constraint(cons)
# s.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)

sg.start()
s.start_constraint("con")
# s.start_constraint("con2")

# print(cons.flag.log.events)
