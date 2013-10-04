# -*- coding:utf-8 -*-

"""
  Settings variables

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 10-25-2012 

  Last modification: 09-20-2013

  Licence: GNU GPL v3
"""

import os
import json

class Settings(object):

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
    self.__progressBar          = None
    self.__external             = ""
    self.__report               = {
      "template" : "",
      "pages"    : "",
      "type"     : "",
      "final"    : "",
    }
    self.__slide                = 0
    self.__exercise_number      = 0
    self.__part_number          = 0
    self.__previous_page        = {}
    self.__filename, self.__ext = os.path.splitext(filename)
    self.__dir                  = {
      "presentation" : presentation_dir,
      "root"         : root_path,
      "slides"       : presentation_dir + "/slides/",
      "report"       : presentation_dir + "/report/",
      "scripts"      : presentation_dir + "/data/scripts",
    }

  def __getTheme(self):
    return self.__theme
  def __setTheme(self, theme):
    self.__theme = theme
  THEME = property(__getTheme, __setTheme)

  def __getCore(self):
    return self.__core
  def __setCore(self, core):
    self.__core = core
  CORE = property(__getCore, __setCore)

  def __getPresentation(self):
    return self.__presentation
  def __setPresentation(self, presentation):
    self.__presentation = presentation
  PRESENTATION = property(__getPresentation, __setPresentation)

  def __getTemplate(self):
    return self.__template
  def __setTemplate(self, template):
    self.__template = template
  TEMPLATE = property(__getTemplate, __setTemplate)
    
  def __getProgressbar(self):
    return self.__progressbar
  def __setProgressbar(self, progressbar):
    self.__progressbar = progressbar
  PROGRESSBAR = property(__getProgressbar, __setProgressbar)
    
  def __getNumbers(self):
    return self.__numbers
  def __setNumbers(self, numbers):
    self.__numbers = numbers
  NUMBERS = property(__getNumbers, __setNumbers)
    
  def __getTransition(self):
    return self.__transition
  def __setTransition(self, transition):
    self.__transition = transition
  TRANSITION = property(__getTransition, __setTransition)
    
  def __getLang(self):
    return self.__lang
  def __setLang(self, lang):
    self.__lang = lang
  LANG = property(__getLang, __setLang)
    
  def __getTitle(self):
    return self.__title
  def __setTitle(self, title):
    self.__title = title
  TITLE = property(__getTitle, __setTitle)

  def __getAuthor(self):
    return self.__author
  def __setAuthor(self, author):
    self.__author = author
  AUTHOR = property(__getAuthor, __setAuthor)

  def __getMail(self):
    return self.__mail
  def __setMail(self, mail):
    self.__mail = mail
  MAIL = property(__getMail, __setMail)

  def __getTwitter(self):
    return self.__twitter
  def __setTwitter(self, twitter):
    self.__twitter = twitter
  TWITTER = property(__getTwitter, __setTwitter)

  def __getConst(self):
    return json.load(open(self.DIR["root"] + "i18n/const.json"))
  CONST = property(__getConst)

  def __getProgressBar(self):
    return self.__progressBar
  def __setProgressBar(self, progressBar):
    self.__progressBar = progressBar
  CONSOLE_PROGRESS_BAR = property(__getProgressBar, __setProgressBar)

  def __getExternal(self):
    return self.__external
  def __setExternal(self, link):
    self.__external = link
  EXTERNAL = property(__getExternal, __setExternal)

  def __getReport(self):
    return self.__report
  REPORT = property(__getReport)
    
  def __getExerciseNumber(self):
    return self.__exercise_number
  def __setExerciseNumber(self, exercise_number):
    self.__exercise_number = exercise_number
  EXERCISE_NUMBER = property(__getExerciseNumber, __setExerciseNumber)

  def __getPartNumber(self):
    return self.__part_number
  def __setPartNumber(self, part_number):
    self.__part_number = part_number
  PART_NUMBER = property(__getPartNumber, __setPartNumber)

  def __getSlide(self):
    return self.__slide
  def __setSlide(self, slide):
    self.__slide = slide
  SLIDE = property(__getSlide, __setSlide)
    
  def __getPrevious_page(self):
    return self.__previous_page
  def __setPrevious_page(self, previous_page):
    self.__previous_page = previous_page
  PREVIOUS_PAGE = property(__getPrevious_page, __setPrevious_page)
    
  def __getFilename(self):
    return self.__filename
  FILENAME = property(__getFilename)
    
  def __getExt(self):
    return self.__ext
  EXT = property(__getExt)
    
  def __getDir(self):
    return self.__dir
  DIR = property(__getDir)
