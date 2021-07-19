from enum import Enum


class ConstraintStatus(Enum):
    """This describes the status of the constraint/model"""

    # constraint has been passed some inputs
    INPUT_PASSED = "input_passed"

    # constraint/model has not been started
    NOT_STARTED = "not started"

    # model is doing some work
    ACTIVE = "active"

    # an error occured with a model
    ERROR = "error"

    # model has been paused
    PAUSED = "paused"

    # model has resumed
    RESUMED = "resumed"

    # model is waiting for external input
    PENDING_INPUT = "pending_input"

    # model has completed work and its output has been saved
    COMPLETE = "complete"

    # model has produced some output
    OUTPUT_PRODUCED = "output_produced"
