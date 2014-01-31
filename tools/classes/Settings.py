# -*- coding:utf-8 -*-

"""
  Settings variables

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 10-25-2012

  Last modification: 01-22-2014

  Licence: GNU GPL v3
"""

import os
import json


class Settings(object):
    """
        Global settings definition
    """

    def __init__(self, filename, root_path):
        """
            Constructor

            :param filename:  Name of the yaml file containing the presentation
            :type  filename:  string
      
            :param root_path: Path of the script executed
            :type  root_path: string
      
            :return: Object Settings
            :rtype:  Settings
        """
        presentation_dir = os.path.dirname(filename)
        if presentation_dir == "" or \
             (presentation_dir[0] != '/' and presentation_dir[0] != "."):
            presentation_dir = "./" + presentation_dir

        self.__theme                = ""
        self.__core                 = ""
        self.__presentation         = ""
        self.__template             = ""
        self.__progressbar          = ""
        self.__numbers              = ""
        self.__transition           = ""
        self.__lang                 = ""
        self.__title                = ""
        self.__author               = ""
        self.__mail                 = ""
        self.__twitter              = ""
        self.__const                = None
        self.__progress_bar         = None
        self.__external             = ""
        self.__report               = {
            "template": "",
            "pages": "",
            "type": "",
            "final": "",
        }
        self.__slide                = 0
        self.__exercise_number      = 0
        self.__part_number          = 0
        self.__part_image           = ""
        self.__previous_page        = {}
        self.__filename, self.__ext = os.path.splitext(filename)
        self.__dir                  = {
            "presentation": presentation_dir,
            "root": root_path,
            "slides": presentation_dir + "/slides/",
            "report": presentation_dir + "/report/",
            "scripts": presentation_dir + "/data/scripts",
        }

    def __get_theme(self):
        """
            Accessor for the theme attribute 
        """
        return self.__theme
    def __set_theme(self, theme):
        """
            Modifier for the theme attribute 
        """
        self.__theme = theme
    THEME = property(__get_theme, __set_theme)

    def __get_core(self):
        """
            Accessor for the core attribute 
        """
        return self.__core
    def __set_core(self, core):
        """
            Modifier for the core attribute 
        """
        self.__core = core
    CORE = property(__get_core, __set_core)

    def __get_presentation(self):
        """
            Accessor for the presentation attribute 
        """
        return self.__presentation
    def __set_presentation(self, presentation):
        """
            Modifier for the presentation attribute 
        """
        self.__presentation = presentation
    PRESENTATION = property(__get_presentation, __set_presentation)

    def __get_template(self):
        """
            Accessor for the template attribute 
        """
        return self.__template
    def __set_template(self, template):
        """
            Modifier for the template attribute 
        """
        self.__template = template
    TEMPLATE = property(__get_template, __set_template)
    
    def __get_progressbar(self):
        """
            Accessor for the progressbar attribute 
        """
        return self.__progressbar
    def __set_progressbar(self, progressbar):
        """
            Modifier for the progressbar attribute 
        """
        self.__progressbar = progressbar
    PROGRESSBAR = property(__get_progressbar, __set_progressbar)
    
    def __get_numbers(self):
        """
            Accessor for the numbers attribute 
        """
        return self.__numbers
    def __set_numbers(self, numbers):
        """
            Modifier for the numbers attribute 
        """
        self.__numbers = numbers
    NUMBERS = property(__get_numbers, __set_numbers)
    
    def __get_transition(self):
        """
            Accessor for the transition attribute 
        """
        return self.__transition
    def __set_transition(self, transition):
        """
            Modifier for the transition attribute 
        """
        self.__transition = transition
    TRANSITION = property(__get_transition, __set_transition)
    
    def __get_lang(self):
        """
            Accessor for the lang attribute 
        """
        return self.__lang
    def __set_lang(self, lang):
        """
            Modifier for the lang attribute 
        """
        self.__lang = lang
    LANG = property(__get_lang, __set_lang)
    
    def __get_title(self):
        """
            Accessor for the title attribute 
        """
        return self.__title
    def __set_title(self, title):
        """
            Modifier for the title attribute 
        """
        self.__title = title
    TITLE = property(__get_title, __set_title)

    def __get_author(self):
        """
            Accessor for the author attribute 
        """
        return self.__author
    def __set_author(self, author):
        """
            Modifier for the author attribute 
        """
        self.__author = author
    AUTHOR = property(__get_author, __set_author)

    def __get_mail(self):
        """
            Accessor for the mail attribute 
        """
        return self.__mail
    def __set_mail(self, mail):
        """
            Modifier for the mail attribute 
        """
        self.__mail = mail
    MAIL = property(__get_mail, __set_mail)

    def __get_twitter(self):
        """
            Accessor for the twitter attribute 
        """
        return self.__twitter
    def __set_twitter(self, twitter):
        """
            Modifier for the twitter attribute 
        """
        self.__twitter = twitter
    TWITTER = property(__get_twitter, __set_twitter)

    def __get_const(self):
        """
            Accessor for the const attribute 
        """
        return json.load(open(self.DIR["root"] + "i18n/const.json"))
    CONST = property(__get_const)

    def __get_progress_bar(self):
        """
            Accessor for the porgress_bar attribute 
        """
        return self.__progress_bar
    def __set_progress_bar(self, progress_bar):
        """
            Modifier for the porgress_bar attribute 
        """
        self.__progress_bar = progress_bar
    CONSOLE_PROGRESS_BAR = property(__get_progress_bar, __set_progress_bar)

    def __get_external(self):
        """
            Accessor for the external attribute 
        """
        return self.__external
    def __set_external(self, link):
        """
            Modifier for the external attribute 
        """
        self.__external = link
    EXTERNAL = property(__get_external, __set_external)

    def __get_report(self):
        """
            Accessor for the report attribute 
        """
        return self.__report
    REPORT = property(__get_report)
    
    def __get_exercise_number(self):
        """
            Accessor for the exercise_number attribute 
        """
        return self.__exercise_number
    def __set_exercise_number(self, exercise_number):
        """
            Modifier for the exercise_number attribute 
        """
        self.__exercise_number = exercise_number
    EXERCISE_NUMBER = property(__get_exercise_number, __set_exercise_number)

    def __get_part_number(self):
        """
            Accessor for the part_number attribute 
        """
        return self.__part_number
    def __set_part_number(self, part_number):
        """
            Modifier for the part_number attribute 
        """
        self.__part_number = part_number
    PART_NUMBER = property(__get_part_number, __set_part_number)

    def __get_part_image(self):
        """
            Accessor for the part_image attribute 
        """
        return self.__part_image
    def __set_part_image(self, part_image):
        """
            Modifier for the part_image attribute 
        """
        self.__part_image = part_image
    PART_IMAGE = property(__get_part_image, __set_part_image)

    def __get_slide(self):
        """
            Accessor for the slide attribute 
        """
        return self.__slide
    def __set_slide(self, slide):
        """
            Modifier for the slide attribute 
        """
        self.__slide = slide
    SLIDE = property(__get_slide, __set_slide)
    
    def __get_previous_page(self):
        """
            Accessor for the previous_page attribute 
        """
        return self.__previous_page
    def __set_previous_page(self, previous_page):
        """
            Modifier for the previous_page attribute 
        """
        self.__previous_page = previous_page
    PREVIOUS_PAGE = property(__get_previous_page, __set_previous_page)
    
    def __get_filename(self):
        """
            Accessor for the filename attribute 
        """
        return self.__filename
    FILENAME = property(__get_filename)
    
    def __get_ext(self):
        """
            Accessor for the ext attribute 
        """
        return self.__ext
    EXT = property(__get_ext)
    
    def __get_dir(self):
        """
            Accessor for the dir attribute 
        """
        return self.__dir
    DIR = property(__get_dir)
