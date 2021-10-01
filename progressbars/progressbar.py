from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import *


def displayTime(time: float) -> str:
    time = datetime.fromtimestamp(time, timezone.utc)
    return f"{str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}:{str(time.second).zfill(2)}"

class ProgressIterator:
    def __init__(self, progressBar: ProgressBar) -> None:
        self.__index = 0
        self.__progressBar = progressBar
        self.__iterableLength = len(self.__progressBar.iterable)
        self.__updateInterval = progressBar.updateInterval
        self.__start = time.time()
    
    def __next__(self) -> Any:
        runCycle = (self.__index % self.__updateInterval == 0 or self.__index == self.__iterableLength - 1) and self.__iterableLength > 0

        if self.__index > 0 and runCycle:
            print(end="\033[1A")

        if runCycle:
            terminalWidth = os.get_terminal_size().columns

            percentage = str(int((self.__index + 1) / self.__iterableLength * 100)) + "%"
            ratio = f"{self.__index + 1}/{self.__iterableLength}"
            elapsed = time.time() - self.__start
            remaining = elapsed
            elapsed = f"Elapsed: {displayTime(elapsed)}"
            remaining = (self.__iterableLength - self.__index) * (remaining / (self.__index + 1)) + 0.65
            remaining = f"Remaining: {displayTime(remaining)}"

            infoItems = [
                percentage,
                ratio,
                elapsed,
                remaining
            ]

            barWidth = terminalWidth - len(percentage) - len(ratio) - len(elapsed) - len(remaining) - 3 * len(infoItems)

            fullBlocks = (self.__index + 1) /  self.__iterableLength
            decimal = fullBlocks * barWidth - int(fullBlocks * barWidth)
            fullBlocks = int(fullBlocks * barWidth)

            # |███      |
            # |███░     |
            # |███▒     |
            # |███▓     |
            out = "|"
            blocks = "█" * fullBlocks
            if decimal * len("░░▒▓") > 0:
                blocks += "░░▒▓"[min(round(decimal * len("░░▒▓")), len("░░▒▓") - 1)]
            blocks += " " * (barWidth - len(blocks))
            out += blocks
            out += "| "

            # 76% | 201/253 | Elapsed: 00:23:01 | Remaining: 00:06:34
            out += " | ".join(infoItems)

        if self.__index < self.__iterableLength:
            if runCycle:
                print(out)
            item = self.__progressBar.iterable[self.__index]
            self.__index += 1
            return item
        raise StopIteration

class ProgressBar:
    def __init__(self, iterable: Iterable, updateInterval: int = 1) -> None:
        """Creates an iterable progress bar, when iterated over it will update and print the progress bar.

        Args:
            iterable (Iterable): The object to iterate over.
            updateInterval (int, optional): The interval inbetween updates, choosing to update the progress bar less often might be faster. Defaults to 1.
        """
        
        self.iterable = iterable
        self.updateInterval = updateInterval
    
    def __iter__(self) -> ProgressIterator:
        return ProgressIterator(self)
