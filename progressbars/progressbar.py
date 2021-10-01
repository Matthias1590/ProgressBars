from __future__ import annotations

import os
import time
from typing import *

from termcolor import colored

from progressbars import widgets


class ProgressIterator:
    def __init__(self, progressBar: ProgressBar) -> None:
        self.__index = 0
        self.__progressBar = progressBar
        self.__iterableLength = len(self.__progressBar.iterable)
        self.__updateInterval = progressBar.updateInterval
        if self.__updateInterval == None:
            self.__updateInterval = max(1, round(self.__iterableLength / 1000))
        self.__start = time.time()
        self.__lastIteration = self.__start
        self.lastIterationSpeeds = []
        self.color = self.__progressBar.color
        self.averageSampleSize = round(self.__iterableLength / 100)

        for widget in progressBar.widgets:
            widget.progressBar = self
    
    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        runCycle = (self.__index % self.__updateInterval == 0 or self.__index == self.__iterableLength - 1) and self.__iterableLength > 0

        if self.__index > 0 and runCycle and self.__index != self.__iterableLength:
            print(end="\033[1A")

        if runCycle:
            terminalWidth = os.get_terminal_size().columns

            self.percentage = str(int((self.__index + 1) / self.__iterableLength * 100)) + "%"
            self.ratio = f"{self.__index + 1}/{self.__iterableLength}"
            self.elapsed = time.time() - self.__start
            self.remaining = (self.__iterableLength - self.__index) * (self.elapsed/ (self.__index + 1)) + 0.65
            if self.__index > 0:
                self.lastIterationSpeeds.append(time.time() - self.__lastIteration)
            iterationSpeedsLength = len(self.lastIterationSpeeds)
            if iterationSpeedsLength > 0:
                if iterationSpeedsLength > self.averageSampleSize:
                    self.lastIterationSpeeds = self.lastIterationSpeeds[-self.averageSampleSize:]
                self.iterationSpeed = sum(self.lastIterationSpeeds) / iterationSpeedsLength
            else:
                self.iterationSpeed = 0

            barWidth = terminalWidth - 2

            suffix = ""
            for i, widget in enumerate(self.__progressBar.widgets):
                strWidget = str(widget)
                suffix += strWidget
                if i != len(self.__progressBar.widgets) - 1:
                    suffix += " | "
            if suffix != "":
                barWidth -= len(suffix) + 1

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
            out += "|"
            if suffix != "":
                out += " "

            out += suffix

        self.__lastIteration = time.time()

        if self.__index < self.__iterableLength:
            if runCycle:
                if self.color != None:
                    coloredOut = ""
                    for char in out:
                        if char.isdigit():
                            coloredOut += colored(char, self.color)
                        else:
                            coloredOut += char
                    out = coloredOut
                print(out)
            item = self.__progressBar.iterable[self.__index]
            self.__index += 1
            return item
        raise StopIteration

class ProgressBar:
    def __init__(self, widgets: List[widgets.Widget] = [widgets.Percentage, widgets.IterationSpeed, widgets.Counter, widgets.ElapsedTime, widgets.RemainingTime], updateInterval: Optional[int] = None, color: Optional[str] = None) -> None:
        self.widgets = []
        self.updateInterval = updateInterval
        self.color = color
        for widget in widgets:
            self.widgets.append(widget(self))
    
    def __call__(self, iterable: Iterable) -> ProgressIterator:
        self.iterable = iterable
        return ProgressIterator(self)