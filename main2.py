from task_main.task import Task
from constraints.models.example_models.time_model import TimeModel
from constraint_models.product_description_model import ProductDescriptionModel
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
    return CustomConstraint("con", "desc", TimeModel(), is_admin_input_required=False, debug=True)


def createCon2():
    return CustomConstraint("con2", "desc", ChatModel(), is_admin_input_required=False, debug=False)


def createCon3():
    return CustomConstraint("con3", "desc", KeywordModel(), is_admin_input_required=False, debug=True)


def func(constraint_name, command, data, args):
    print(args)
    return input("msg: ")


def func1(data, args):
    print(data)
    # pass


pd = CustomConstraint("cons", "desc", ProductDescriptionModel(),
                      is_admin_input_required=False, debug=True)
task = Task("product name", "prodct desc")
pd.set_task_instance(task)
pd.start()

cons = createCon1()
# cons.add_input(1)
# cons.start()
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
# sg.start()
# s.start_constraint("con")
