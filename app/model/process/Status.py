from enum import Enum


class Status(Enum):
    RUNNING = "RUNNING"
    READY = "READY"
    COMPLETED = "COMPLETED"

    __str__ = lambda self: self.value
