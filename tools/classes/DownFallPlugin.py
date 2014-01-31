# -*- coding:utf-8 -*-

"""
  DownFall Plugin general management

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 10-10-2013

  Last modification: 01-22-2014

  Licence: GNU GPL v3
"""


class DownFallPlugin(object):
    """
        Management class for plugins
    """

    def __init__(self, name):
        """
            Constructor
        """
        self.__name = name

    def __get_name(self):
        """
            Accessor for the name attribute
        """
        return self.__name
    name = property(__get_name)

    def pre(self):
        """
            Code executed before genertaion of slides
        """
        pass

    def post(self):
        """
            Code exectuted after generation of slides
        """
        pass
