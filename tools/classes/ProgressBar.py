# -*- coding:utf-8 -*-

"""
  Progress Bar used in the console in "quiet" mode

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 07-18-2013

  Last modification: 01-22-2014

  Licence: GNU GPL v3
"""

import sys


class ProgressBar(object):
    """
        Progress bar definition (used in console mode)
    """

    colorList = {
        "red": 1,
        "yellow": 3,
        "green": 2,
        "magenta": 5,
    }

    def __init__(self, number):
        self.__current = 0
        self.__max = number
        self.__done = {}

    def incMax(self, number):
        """
            Increment max counter with number unities

            :param number: Incrementation value
            :type  number: int
        """
        self.__max += number

    def decCurrent(self):
        """
            Decrement current counter
        """
        self.__current -= 1

    def incCurrent(self):
        """
            Increment current counter
        """
        self.__current += 1

    def display(self, info=""):
        """
            Display the progress bar

            :param info: Message to display near progress bar
            :type  info: string
        """
        if not info in self.__done:
            self.incCurrent()
            self.__done[info] = True
        progress = (self.__current * 100) / self.__max

        if progress < 35:
            color = ProgressBar.colorList["red"]
        elif progress < 70:
            color = ProgressBar.colorList["magenta"]
        elif progress < 90:
            color = ProgressBar.colorList["yellow"]
        else:
            color = ProgressBar.colorList["green"]

        if self.__current != 1:
            sys.stdout.write("\r")
        sys.stdout.write(
          "Generating \033[34m%-10s\033[39m : [\033[3%dm%-60s\033[39m] %3d%%" %
          (info, color, "#" * (int((float(progress) / 100) * 60)), progress))
        sys.stdout.flush()

    def finish(self):
        """
            Display end of line
        """
        sys.stdout.write("\n")
