# -*- coding:utf-8 -*-

"""
  DownFall Plugin general management

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 10-10-2013 

  Last modification: 10-10-2013

  Licence: GNU GPL v3
"""

class DownFallPlugin(object):

    def __init__(self, name):
        """
        """
        self.__name = name

    def __getName(self):
        return self.__name
    name = property(__getName) 

    def pre(self):
        """
        """
        pass

    def post(self):
        """
        """
        pass
