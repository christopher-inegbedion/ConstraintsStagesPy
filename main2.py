from constraints.models.example_models.product_description_model import ProductDescriptionModel
from multiprocessing.spawn import freeze_support
from constraints.models.example_models.chat_model import ChatModel
from constraints.models.example_models.keyword_model import KeywordModel
from time import sleep, time
from multiprocessing import Process

# from task_main.task import Task
from constraints.models.example_models.internet_model import InternetModel
from constraints.models.example_models.test_model import TestModel
from stage.stage import Stage, StageGroup
from constraints.models.example_models.pause_thread import PauseModel
from constraints.constraint_main.custom_constraint import CustomConstraint
# from task_pipeline.pipeline import Pipeline


def createCon1():
    return CustomConstraint("con", "desc", ProductDescriptionModel(), debug=True)


def createCon2():
    return CustomConstraint("con2", "desc", ChatModel(), debug=False)


def createCon3():
    return CustomConstraint("con3", "desc", KeywordModel(), debug=True)


def func(constraint_name, command, data, args):
    print(args)
    return input("msg: ")


def func1(data, args):
    print(data)
    # pass


cons = createCon1()
cons1 = createCon2()
cons3 = createCon3()

# cons3.add_configuration_input("sds", "passcode")
# cons3.add_configuration_input("sds")


# cons1.add_input("NGN")
# cons1.add_input("USD")

s = Stage('s', display_log=False)
# s.add_constraint(cons)
s.add_constraint(cons)

# s2 = Stage('s2')
# cons = createCon1()
# cons.add_input("EUR")
# cons.add_input("USD")
# cons1 = createCon2()
# cons1.add_input(1)
# s2.add_constraint(cons)
# s2.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)
sg.start()
s.start_constraint("con")
print(s.get_constraint("con").configuration_inputs)

# s.start()
# s.start_constraint("con")
# con = s.get_constraint("con2")
# # con.start_listen()
# # sleep(1)
# con.send_listen_data("user", "hello")
# con.send_listen_data("admin", "hi")
# con.send_listen_data("user", "how are u")
# s.start_constraint("con2")
# s.get_constraint("con2").start_admin()

# sg.add_stage(s2)
# sg.add_stage(s2)

# sg.start('s')

# s.start_constraint("con")
# s.start_constraint("con2")


# pipe = Pipeline(Task("name", "desc"), sg)
# pipe.start_stage("s")
# pipe.start_constraint("s", "con3")
# pipe.start_constraint("s2", "con")
# print(sg.get_stage_group_details())
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
