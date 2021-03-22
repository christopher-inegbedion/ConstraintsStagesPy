from constraints.models.example_models.test_model import TestModel
from stage.stage import Stage, StageGroup
from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint

cons = CustomConstraint("con", PauseModel())
cons1 = CustomConstraint("con2", TestModel())
cons.add_input(12)
cons1.add_input(1)

s = Stage('s')
s.add_constraint(cons)
s.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)

sg.start()
s.start_constraint("con")
s.start_constraint("con2")

# print(cons.flag.log.events)
