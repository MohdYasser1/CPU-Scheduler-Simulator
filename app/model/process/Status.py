from enum import Enum


class Status(Enum):
    RUNNING = "RUNNING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    NOT_ARRIVED = "NOT_ARRIVED"

    __str__ = lambda self: self.value
