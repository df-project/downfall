# -*- coding:utf-8 -*-

"""
  Generation of presentation

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 09-26-2013 

  Last modification: 09-30-2013

  Licence: GNU GPL v3
"""

import logging
import distutils.dir_util
import distutils.file_util
import os
import shutil

from Error import *
from Slide import *


class Presentation(object):
  
  def __init__(self, settings, stream, report, length):
    """
      Constructor

      :param settings:  Settings list including ROOT, LANG, TEMPLATE, etc.
      :type  settings:  string
      
      :param stream:    Data from the yaml file
      :type  stream:    dictionnary

      :param report:    Flag indicating if report is needed
      :type  report:    boolean
      
      :return: Object Presentation
      :rtype:  Presentation
    """
    self.__settings = settings
    self.__stream   = stream
    self.__doc      = None
    self.report     = report
    if length == None:
      self.__length = None
    else:
      self.__length   = length + 1 if self.report else length
    # Define logger
    self.logger = logging.getLogger("downfall_log.Presentation")


  def __getSettings(self):
    return self.__settings
  def __setSettings(self, value):
    self.__settings = value
  settings = property(__getSettings, __setSettings)


  def __getStream(self):
    return self.__stream
  stream = property(__getStream)


  def __getDoc(self):
    return self.__doc
  def __setDoc(self, value):
    self.__doc = value
  doc = property(__getDoc, __setDoc)


  def __getLength(self):
    return self.__length
  length = property(__getLength)


  def setTitle(self):
    """
      Get title and author from yaml stream
    """
    self.settings.TITLE = self.doc.get("title", "Downfall presentation")
    self.settings.AUTHOR = self.doc.get("author", "John Doe")
    self.settings.MAIL = self.doc.get("mail", "")
    self.settings.TWITTER = self.doc.get("twitter", "")


  def setExtensions(self):
    """
      Get extensions from yaml stream
    """
    self.settings.MATH = self.doc.get("math", "")


  def setTheme(self):
    """
      Get theme and copy of related data in presentation directory
    """
    self.settings.THEME = self.doc.get("theme", "downfall")
    self.logger.info("Configuration : theme %s selected" % 
      (self.settings.THEME,))
    # Copy of theme data in data directory of the presentation
    try:
      distutils.dir_util.copy_tree(self.settings.DIR['root'] + "../themes/" + 
        self.settings.THEME, self.settings.DIR["presentation"] + "/data")  
    except IOError:
      self.logger.critical("Can't copy themes directory in data directory")
      exit(Error.IOFILE)
    # Copy of the LaTeX class if report wanted
    if self.report:
      try:
        distutils.file_util.move_file(self.settings.DIR["presentation"] +
          "/data/report/df-report.cls", self.settings.DIR["presentation"])
      except IOError:
        self.logger.critical("Can't copy LaTeX class " +
                             "in presentation directory")
        exit(Error.IOFILE)


  def setLanguage(self):
    """
      Set the language to use to generate presentation
    """
    self.settings.LANG = self.doc.get("lang", "")
    info_lang = "Language : "
    if self.settings.LANG != "":
      info_lang += self.settings.LANG
      self.settings.LANG = "_" + self.settings.LANG
      self.settings.LANG_CONST = self.settings.LANG
    else:
      info_lang +=  " default language"
      self.settings.LANG_CONST = self.settings.CONST["default"]
    info_lang +=  " selected"
    self.logger.info(info_lang)


  def setCore(self):
    """
      Set the core to use to generate presentation
    """
    self.settings.CORE  = self.doc.get("core", "downfall")
    self.logger.info( "Configuration : core %s selected" % 
      (self.settings.CORE,))


  def setProgressBar(self):
    """
      Detect and set the progress bar in the presentation slides
    """
    if self.doc.get("progressbar", False):
      if self.settings.CORE == "downfall":
        self.settings.PROGRESSBAR = '<div class="progress"><div></div></div>'


  def setNumbering(self):
    """
      Set if number of slides will be displayed
    """
    if not self.doc.get("numbers", True):
      self.settings.NUMBERS = "nonumbers"


  def setTransition(self):
    """
      Set transition between slides
    """
    self.settings.TRANSITION = self.doc.get("transition", "")


  def setLabels(self):
    """
      Set labels report in case of modification
    """
    if self.report:
      self.settings.EXERCISES = self.doc.get("exercise_label", "")
      if self.settings.EXERCISES == "":
        self.settings.EXERCISES_CHANGE = False
      else:
        self.settings.EXERCISES_CHANGE = True
      self.settings.DEFINITIONS = self.doc.get("definition_label", "")
      if self.settings.DEFINITIONS == "":
        self.settings.DEFINITIONS_CHANGE = False
      else:
        self.settings.DEFINITIONS_CHANGE = True


  def setTOC_Index(self):
    """
      Activate (or not) table of contents and index
    """
    if self.report:
      # Detection of table of contents report display
      self.settings.TOC = self.doc.get("tableofcontents", False)
      # Detection of index report display
      self.settings.INDEX = self.doc.get("index", False)


  def load_template_report(self, type_slide):
    """
      Load specific template for report

      :param type_slide: Type of slide
      :type  type_slide: string

      :return:           None
    """
    self.settings.REPORT["type"] = type_slide
    try:
      with open(self.settings.DIR['root'] + "../themes/" + 
          self.settings.THEME + "/report/" + self.settings.REPORT["type"] + 
          ".tex") as fic_report:
        self.settings.REPORT["template"] = fic_report.read()
    except IOError:
      self.logger.info("No file %s found in theme %s" % 
        (type_slide, self.settings.THEME))
      exit(Error.IOError)
  
    # Load Second and exercise template for 2slidesnnotes
    if type_slide == "2slidesnnotes":
      try:
        with open(self.settings.DIR['root'] + "../themes/" + 
            self.settings.THEME + "/report/" + "2slides.tex") as fic_report:
          self.settings.REPORT["template_2"] = fic_report.read()
      except IOError:
        main_logger.info("No file %s found in theme %s" % 
          ("2slides", self.settings.THEME))
        exit(Error.IOError)
      try:
        with open(self.settings.DIR['root'] + "../themes/" + 
            self.settings.THEME + "/report/" + "exercise.tex") as fic_report:
          self.settings.REPORT["template_exercise"] = fic_report.read()
      except IOError:
        main_logger.info("No file %s found in theme %s" % 
          ("exercise", self.settings.THEME))
        exit(Error.IOError)

    # Load 1slide template for unique slide
    if type_slide == "2slides" or type_slide == "2slidesnnotes":
      try:
        with open(self.settings.DIR['root'] + "../themes/" + 
            self.settings.THEME + "/report/" + "1slide.tex") as fic_report:
          self.settings.REPORT["template_unique"] = fic_report.read()
      except IOError:
        main_logger.info("No file %s found in theme %s" % 
          ("1slide", self.settings.THEME))
        exit(7)


  def setReportTemplate(self):
    """
      Load report template if needed
    """
    if self.report:
      self.load_template_report(self.doc.get("report", "1slide"))
      try:
        fic_final_report = open(self.settings.DIR['root'] + "../themes/" + 
          self.settings.THEME + "/report/report.tex")
        self.settings.REPORT["final"] = fic_final_report.read()
      except IOError:
        self.logger.critical("No file template report.tex found in " +
          "theme %s" % (self.settings.THEME,))
        exit(Error.IOFILE)
      fic_final_report.close()


  def setScripts(self):
    """
      Copy scripts from the selected core to the presentation directory
    """
    try:
      if not os.path.exists(self.settings.DIR["scripts"]):
        os.makedirs(self.settings.DIR["scripts"])
    except IOError:
      self.logger.critical("Can't create directory %s" %
        (self.settings.DIR["scripts"],))
      exit(Error.IOError)
    
    try:
      shutil.copy(self.settings.DIR['root'] + "cores/" + self.settings.CORE + 
        "/script.js", self.settings.DIR["scripts"])  
    except IOError:
      self.logger.critical("Can't copy scripts in directory %s" %
        (self.settings.DIR["scripts"],))
      exit(Error.IOError)

    """
      Copy KaTeX scripts if math selected
    """
    if self.settings.MATH:
      # Create fonts sub-directory in styles directory
      try:
        if not os.path.exists(self.settings.DIR["styles"] + "/fonts"):
          os.makedirs(self.settings.DIR["styles"] + "/fonts")
      except IOError:
        self.logger.critical("Can't create directory %s" %
          (self.settings.DIR["styles"] + "/fonts",))
        exit(Error.IOError)
      # Copy scripts and style
      try:
        shutil.copy(self.settings.DIR['root'] + "cores/" + self.settings.CORE + 
          "/extensions/katex/scripts/katex.min.js", self.settings.DIR["scripts"]) 
        shutil.copy(self.settings.DIR['root'] + "cores/" + self.settings.CORE + 
          "/extensions/katex/scripts/auto-render.min.js", self.settings.DIR["scripts"]) 
        shutil.copy(self.settings.DIR['root'] + "cores/" + self.settings.CORE + 
          "/extensions/katex/style/katex.min.css", self.settings.DIR["styles"])
      except IOError:
        self.logger.critical("Can't copy KaTeX scripts or styles in directory %s" %
          (self.settings.DIR["scripts"],))
        exit(Error.IOError)
      # Copy fonts in styles/fonts directory
      try:
        distutils.dir_util.copy_tree(self.settings.DIR['root'] + "cores/" + 
          self.settings.CORE + "/extensions/katex/style/fonts", 
          self.settings.DIR["styles"] + "/fonts")  
      except IOError:
        self.logger.critical("Can't copy KaTeX font directory in data/styles/fonts directory")
        exit(Error.IOFILE)


  def nextSlide(self):
    """
      Increment the current slide number
    """
    self.settings.SLIDE += 1


  def generate_html(self):
    """
      Generate html file for the presentation
    """
    try:
      with open(self.settings.FILENAME + ".html", "w") as fic_presentation:
        fic_presentation.write(pystache.render(self.settings.TEMPLATE, 
          {"presentation" : self.settings.PRESENTATION, 
           "progressbar"  : self.settings.PROGRESSBAR,
           "title"        : self.settings.TITLE,
           "author"       : self.settings.AUTHOR,
           "mail"         : self.settings.MAIL,
           "twitter"      : self.settings.TWITTER,
           "math"         : self.settings.MATH,
           "transition"   : self.settings.TRANSITION, 
           "numbers"      : self.settings.NUMBERS}).encode('utf-8'))
    except IOError:
      self.logger.critical("Unable to save the presentation in %s.html" %
        (self.settings.FILENAME,))
      exit(Error.IOError)


  def generate_slides(self):
    """
      Generate presentation slides from self.__stream data
    """
    for self.doc in self.stream:
      if not "type" in self.doc:
        # Configuration of the presentation
        # 1st slide is not a real slide but settings data
        if self.settings.SLIDE == 0:
          """
            Settings
          """
          # Author and title detection
          self.setTitle()
          # Detection of theme
          self.setTheme()
          # Detection of language
          self.setLanguage()
          # Detection of core
          self.setCore()
          # Detection of progressbar
          self.setProgressBar()
          # Detection of numbering
          self.setNumbering()
          # Detection of transition type
          self.setTransition()
          # Detection of report labels modifications
          self.setLabels()
          # Detection of extensions used
          self.setExtensions()
          # Detection of table of contents and index report display
          self.setTOC_Index()
          # Load report template if needed
          self.setReportTemplate()
          # Copy scripts
          self.setScripts()
        else:
          # If a slide has no type and is not the 1st slide, this is a
          # syntax error in the yaml file
          self.logger.critical("Error on slide %d : no type specified" %
            (self.settings.SLIDE,))
          exit(Error.YAML_SYNTAX)
        # Next slide
        self.nextSlide()
      else:
        """
          Slides
        """
        s = Slide(self.settings, self.doc)

        # Slide and report generation
        s.generate_all(self.report)

    # Generate html file of the presentation
    self.generate_html()
 

  def generate_report(self):
    """
      Generation of the report associated to the presentation
    """
    # Copy of the core file in the call directory
    try:
      # Generate final report if needed
      if self.report:
        if (self.settings.REPORT["type"] == "2slides" or 
            self.settings.REPORT["type"] == "2slidesnnotes") and \
            self.settings.PREVIOUS_PAGE:
          # Change report template to use only one slide
          self.settings.REPORT["pages"] += \
            pystache.render(self.settings.REPORT["template_unique"], 
              {"image1" : self.settings.DIR["presentation"] + 
                "/report/slide_%03d" % (self.settings.SLIDE - 1,) })
        # Write final report on file
        self.logger.info("Generating final report")
        fic_report = open(self.settings.FILENAME + ".tex", "w")
        fic_report.write(pystache.render(self.settings.REPORT["final"],
          {"path" : self.settings.DIR["presentation"],
           "filename" : self.settings.FILENAME,
           "title" : self.settings.TITLE,
           "author" : self.settings.AUTHOR,
           "tableofcontents" : self.settings.TOC,
           "index" : self.settings.INDEX,
           "exercise_label" : self.settings.EXERCISES,
           "chg_exercise_label" : self.settings.EXERCISES_CHANGE,
           "definition_label" : self.settings.DEFINITIONS,
           "chg_definition_label" : self.settings.DEFINITIONS_CHANGE,
           "report" : self.settings.REPORT["pages"]}).encode("utf-8"))
    except IOError:
      self.logger.critical("Unable to save the presentation in %s.html" %
      (settings.FILENAME,))
      exit(Error.IOError)
  
    # generation of the report
    if self.report:
      # Progress bar
      if self.settings.CONSOLE_PROGRESS_BAR != None:
        self.settings.CONSOLE_PROGRESS_BAR.display("report")
      base_filename = self.settings.FILENAME.split("/")[-1]
      fic_report.close()
      iterate = 3 if self.settings.TOC else 1
      # Triple compilation for the table of contents
      if self.settings.CONSOLE_PROGRESS_BAR == None:
        log = ""
        log_index = ""
      else:
        log = "1>/dev/null"
        log_index = "2>>%s/%s.log" % (self.settings.DIR["presentation"],
          base_filename)
      for i in range(iterate):
        os.system("pdflatex -shell-escape %s.tex %s" % 
          (self.settings.FILENAME, log))
        # Bug in minted : --output-dir option of pdflatex is not usable
        # os.system("pdflatex -shell-escape --output-dir %s %s.tex" %
        #   (settings.DIR["presentation"], settings.FILENAME))
        # Make index if selected
        if self.settings.INDEX and i == 0:
          os.system(("makeindex -s %s/data/report/styleIndex.ist -i " + 
            "< %s.idx >%s.ind %s") % (self.settings.DIR["presentation"], 
            self.settings.FILENAME, base_filename, log_index))

      # TODO: Breaking compatibility -> remove system call
      # Working files in current directory so we must to move them (always
      # minted bug...)
      os.system("mv %s* %s 2>>%s/%s.log" % (base_filename, 
        self.settings.DIR["presentation"], self.settings.DIR["presentation"], 
        base_filename))

      for fic in (".aux", ".log", ".fdb_latexmk"):
        try:
          self.logger.info("Removing %s" % (self.settings.FILENAME + fic,))
          os.remove(self.settings.FILENAME + fic)
        except OSError:
          self.logger.error( "File %s not found" % 
            (self.settings.FILENAME + fic,))

    # New line after progress bar
    if self.settings.CONSOLE_PROGRESS_BAR != None:
      self.settings.CONSOLE_PROGRESS_BAR.finish()
