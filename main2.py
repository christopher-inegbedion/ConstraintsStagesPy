from time import sleep, time

from task_main.task import Task
from constraints.models.example_models.internet_model import InternetModel
from constraints.models.example_models.test_model import TestModel
from stage.stage import Stage, StageGroup
from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint
from task_pipeline.pipeline import Pipeline


def createCon1():
    return CustomConstraint("con", "desc", InternetModel(), debug=False)


def createCon2():
    return CustomConstraint("con2", "desc", InternetModel(), debug=False)


constraints = {
    "con": createCon1(),
    "con2": createCon2()
}


cons = createCon1()
cons1 = constraints["con2"]
cons.add_input("EUR")
cons.add_input("USD")

cons1.add_input("NGN")
cons1.add_input("USD")

s = Stage('s')
s.add_constraint(cons)

s2 = Stage('s2')
cons = createCon1()
cons.add_input("EUR")
cons.add_input("USD")
cons1 = constraints["con2"]
cons1.add_input("EUR")
cons1.add_input("USD")
s2.add_constraint(cons)
s2.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)
sg.add_stage(s2)
# sg.add_stage(s2)

# sg.start('s')


def update(pipe, args):
    print("update1")


def update2(pipe, args):
    print("update2")

# s.start_constraint("con")
# s.start_constraint("con2")


pipe = Pipeline(Task("name", "desc"), sg)
pipe.start()
pipe.on_update(update)
pipe.on_update(update2)
pipe.start_constraint("s", "con")
print(sg.get_stage_group_details())
# sleep(2)
# pipe.start_constraint("s2", "con")

# pipe.start_stage("s2")


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
