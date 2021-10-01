from abc import ABC, abstractmethod
from datetime import datetime, timezone

def displayTime(time: float) -> str:
    time = datetime.fromtimestamp(time, timezone.utc)
    return f"{str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}:{str(time.second).zfill(2)}"

class Widget(ABC):
    def __init__(self, progressBar) -> None:
        super().__init__()

        self.progressBar = progressBar

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

class Percentage(Widget):
    def __str__(self) -> str:
        return f"{self.progressBar.percentage}"

class Counter(Widget):
    def __str__(self) -> str:
        return f"{self.progressBar.ratio}"

class ElapsedTime(Widget):
    def __str__(self) -> str:
        return f"Elapsed: {displayTime(self.progressBar.elapsed)}"

class RemainingTime(Widget):
    def __str__(self) -> str:
        return f"Remaining: {displayTime(self.progressBar.remaining)}"

class IterationSpeed(Widget):
    def __str__(self) -> str:
        if self.progressBar.iterationSpeed > 0:
            iterationSpeed = 1 / self.progressBar.iterationSpeed
        else:
            iterationSpeed = 0
        return f"{str(round(iterationSpeed, 2))[::-1].zfill(6)[::-1]} it/s"