from abc import ABC, abstractmethod


class SchedulingStrategy(ABC):
    @abstractmethod
    def run(self, scheduler):
        pass
