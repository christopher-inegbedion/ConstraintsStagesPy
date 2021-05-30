from time import sleep, time
from constraints.models.example_models.internet_model import InternetModel
from constraints.models.example_models.test_model import TestModel
from stage.stage import Stage, StageGroup
from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint

cons = CustomConstraint("con", "desc", InternetModel())
cons1 = CustomConstraint("con2", "desc", InternetModel())
cons.add_input("EUR")
cons.add_input("USD")

cons1.add_input("NGN")
cons1.add_input("USD")

s = Stage('s')
s.add_constraint(cons)
s.add_constraint(cons1)

# s2 = Stage("p")
# s2.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)
# sg.add_stage(s2)

sg.start('s')
s.start_constraint("con")
s.start_constraint("con")
s.start_constraint("con2")




# s = Stage('s2')
# cons = CustomConstraint("con", "desc", InternetModel())
# cons1 = CustomConstraint("con2", "desc", InternetModel())
# s.add_constraint(cons)
# s.add_constraint(cons1)
# sg = StageGroup()

# sg.add_stage(s)


# sleep(1)
# cons.add_input("EUR")
# cons.add_input("USD")

# cons1.add_input("NGN")
# cons1.add_input("USD")
# print()
# sg.start('s2')
# sleep(1)

# s.start_constraint("con")
# s.start_constraint("con2")

# print(cons.flag.log.events)
