# -*- coding:utf-8 -*-

"""
  Generation of slides and report

  Author: Tristan Colombo <tristan.colombo@info2dev.com>
                          (@TristanColombo)

  Date: 10-25-2012 

  Last modification: 09-30-2013

  Licence: GNU GPL v3
"""

import pystache
import os
import yaml
import logging
import pygments
import pygments.lexers
import pygments.formatters
import re
import shutil
import itertools 


class Slide(object):
  
  def __init__(self, settings, data):
    """
      Constructor

      :param settings:  Settings list including ROOT, LANG, TEMPLATE, etc.
      :type  settings:  string
      
      :param data:        Data read from the yaml file and used to generate the
                          slide
      :type  data:        dictionnary
      
      :return: Object Slide
      :rtype:  Slide
    """
    self.__settings        = settings
    self.__identifier      = "slide_%03d" % (settings.SLIDE,)
    self.__data            = data
    self.__html            = None

    # Get global template
    if settings.TEMPLATE == "":
      try:
        fic_template = open(settings.DIR['root'] + "cores/" + settings.CORE + 
            "/main.html")
        settings.TEMPLATE = fic_template.read()
      except IOError:
        self.logger.critical("Core template %s not found" % (settings.CORE,))
        exit(3)
      fic_template.close()
    self.__template_main   = settings.TEMPLATE

    # Save the slide number of the link to external slides
    self.__external = None

    # Define logger
    self.logger = logging.getLogger("downfall_log.Slide")


  def __getSettings(self):
    return self.__settings
  settings = property(__getSettings)


  def __get_identifier(self):
    return self.__identifier
  identifier = property(__get_identifier)


  def __get_data(self):
    return self.__data
  data = property(__get_data)


  def __get_lang(self):
    return self.__settings.LANG
  lang = property(__get_lang)


  def __get_html(self):
    return self.__html
  def __set_html(self, html):
    self.__html = html
  html = property(__get_html, __set_html)


  def __get_theme(self):
    return self.__settings.THEME
  theme = property(__get_theme)


  def __get_template_main(self):
    return self.__template_main
  def __set_template_main(self, template_main):
    self.__template_slide = template_main
  template_main = property(__get_template_main, __set_template_main)


  def __get_template_report(self):
    return self.__settings.REPORT["template"]
  def __set_template_report(self, template_report):
    self.__settings.REPORT["template"] = template_report
  template_report = property(__get_template_report, __set_template_report)


  def __get_template_report_2(self):
    return self.__settings.REPORT["template_2"]
  def __set_template_report_2(self, template_report_2):
    self.__settings.REPORT["template_2"] = template_report_2
  template_report_2 = property(__get_template_report_2, __set_template_report_2)


  def __get_template_report_unique(self):
    return self.__settings.REPORT["template_unique"]
  def __set_template_report_unique(self, template_report_unique):
    self.__settings.REPORT["template_unique"] = template_report_unique
  template_report_unique = property(__get_template_report_unique, 
    __set_template_report_unique)


  def __get_template_report_exercise(self):
    return self.__settings.REPORT["template_exercise"]
  def __set_template_report_exercise(self, template_report_exercise):
    self.__settings.REPORT["template_exercise"] = template_report_exercise
  template_report_exercise = property(__get_template_report_exercise, 
    __set_template_report_exercise)


  def __get_report_type(self):
    return self.__settings.REPORT["type"]
  report_type = property(__get_report_type)


  def __get_root_dir(self):
    return self.__settings.DIR["root"]
  root_dir = property(__get_root_dir)


  def __get_slides_dir(self):
    return self.__settings.DIR["slides"]
  slides_dir = property(__get_slides_dir)


  def __get_report_dir(self):
    return self.__settings.DIR["report"]
  report_dir = property(__get_report_dir)


  def __getExternal(self):
    return self.__external
  def __setExternal(self, external):
    self.__external = external
  external = property(__getExternal, __setExternal)


  def __replace(self):
    """
      Modify the self.data dictionnary for special cases

      :return: None
    """
    # In case of list create a dictionnary from yaml data
    if "list" in self.data:
      bullets_list = self.data["list"].rstrip().split("\n")
      # In the animated list we pop the first element of the list
      # to activate him separately
      if self.data["type"] == "animatedlist":
        self.data["first"] = bullets_list.pop(0)

      self.data["list"] = map(lambda x: {"bullet": x}, bullets_list) 

    # If "credit" is complete, automatically activate the inclusion
    # of the credits in the bottom of the page
    if "credit" in self.data:
      self.data["include_credits"] = True

    # On "fullvideo" slides, report is disabled
    if self.data["type"] == "fullvideo":
      self.data["report"] = "hide"

    # On "fullimage" slides, background-text by default and not full line
    if self.data["type"] == "fullimage":
      self.data["background-text"] = self.data.get("background-text", True)
      self.data["fulline"] = self.data.get("fullline", False)

    # On exercise_title slide, determine number of the exercise
    if self.data["type"] == "exercise_title":
      # Saving the title of the exercise
      self.settings.EXERCISE_NAME = self.data["title"]
      self.settings.EXERCISE_NUMBER += 1
      if self.settings.PART_NUMBER != 0:
        self.data["number"] = "%d.%d" % (self.settings.PART_NUMBER,
            self.settings.EXERCISE_NUMBER)
        # Use same image as part if no image defined
        if not "image" in self.data:
          self.data["image"] = self.settings.PART_IMAGE
      else:
        self.data["number"] = self.settings.EXERCISE_NUMBER
      self.data["exercise"] = \
          self.settings.CONST["exercise"][self.settings.LANG_CONST]
    
    # On part slide, determine number of the part
    if self.data["type"] == "part":
      self.settings.PART_NUMBER += 1
      self.settings.EXERCISE_NUMBER = 0
      self.data["number"] = self.settings.PART_NUMBER
      self.data["part"] = \
          self.settings.CONST["part"][self.settings.LANG_CONST]
      # Save image path if defined
      if "image" in self.data:
        self.settings.PART_IMAGE = self.data["image"]

    # On exercise slide, determine number of the exercise
    if self.data["type"] == "exercise":
      self.data["title"] = self.settings.EXERCISE_NAME

    # If images, video or code in slide, copy images in data/images,
    # video in data/video or code in data/files and change path
    for tag in ("image", "video", "logo", "file"):
      if tag in self.data:
        if tag == "file":
          target = "data/files/"
        elif tag == "video":
          target = "data/video/"
        else:
          target = "data/images/"
        image_file = target + self.data[tag].split("/")[-1]
        image_file_path = self.settings.DIR["presentation"] + "/" + image_file
        if self.data[tag][0] != "/":
          repository = os.getenv("DF_REPOSITORY")
          if repository != None and os.path.isfile(repository + "/" +
              self.settings.EXTERNAL + "/" + self.data[tag]):
            self.data[tag] = repository + "/" + self.settings.EXTERNAL + \
              "/" + self.data[tag]
          else:
            self.data[tag] = self.settings.DIR["presentation"] + "/" + \
              self.data[tag]
        if not os.path.exists(image_file_path):
          shutil.copy(self.data[tag], image_file_path)
        self.data[tag] = image_file

    # On images, if text near image, display new lines on slides
    if "text_near_image" in self.data:
      self.data["text_near_image"] = \
        self.data["text_near_image"].replace("\n", "<br />\n")

    # On citations, display new lines on slides
    if self.data["type"] == "cite":
      self.data["text"] = \
        self.data["text"].replace("\n", "<br />\n")


  def save(self):
    """
      Save the current slide in the slides_dir directory

      :return: None
    """
    # In case of image in slide, modification of relatives paths
    if "image" in self.data or "logo" in self.data:
      pattern = '<img.*src="(?P<source>[a-zA-Z0-9_][a-zA-Z0-9\-_\/\.]*)"'
      self.html = re.sub(pattern, '<img src="../\g<source>"', self.html)
    if self.data["type"] == "animatedlist":
      pattern = '(class="inner"|class="active")'
      self.html = re.sub(pattern, '', self.html)
    try:
      fic_current_slide = open(self.slides_dir + self.identifier + ".html", "w")
      fic_current_slide.write(pystache.render(self.template_main, 
        {"presentation" : self.html, "path" : "../", "id" : self.identifier,
         "progressbar" : "", "numbers" : "nonumbers", "report":
         "true"}).encode('utf-8'))
    except IOError:
      self.logger.critical("Unable to save the slide %s.html" %
        (self.identifier,))
      exit(5)
    fic_current_slide.close()



  def generate_slide(self):
    """
      Generation of the html code of the slide in the self.html attribute

      :return: None
    """
    self.logger.info("Work in progress : %s" % (self.identifier,))

    # Progress bar
    if self.settings.CONSOLE_PROGRESS_BAR != None:
      self.settings.CONSOLE_PROGRESS_BAR.display(self.identifier)

    # Detection of external slide(s)
    if self.data['type'] == 'external':
      self.logger.info("External slides detected in %s.yaml" %
        (self.data['link'],))
      self.external = self.identifier
      self.generate_external_slides()
      self.logger.info("End of external slides")
      return None

    # Detection of code slide(s)
    if self.data["type"] == "code":
      self.logger.info("Code slides detected")
      self.generate_code_slides()
      self.logger.info("End of code slides")
      return None
    # For code on multi slides activate the slide "code"
    if self.data["type"] == "multicode":
      self.data["type"] = "code"

    # Detection of cover slide
    if self.data["type"] == "cover":
      self.settings.TITLE = self.data.get("title", self.settings.TITLE)
      self.settings.AUTHOR = self.data.get("author", self.settings.AUTHOR)
    # Replacement of special data types
    self.__replace()

    # Using data from doc with pystache
    try:
      fic_template_slide = open(self.root_dir + "../themes/" + self.theme + \
          "/slides/" + self.data["type"] + ".html", "r")
      template_slide = fic_template_slide.read()
    except IOError:
      self.logger.critical("The type %s is not defined in theme %s" % 
        (self.data['type'], self.theme))
      exit(4)
    fic_template_slide.close()

    # Replacement of data in the template using Pystache
    preserve = ("id", "type")
    self.data["id"] = self.identifier
    for key in self.data:
      if not key in preserve and not key.endswith(self.lang):
        self.data[key] = self.data.get(key + self.lang, None)
    self.html = pystache.render(template_slide, self.data)
      
    # Add the current slide to the presentation
    self.settings.PRESENTATION += self.html



  def generate_code_slides(self):
    """
      Generation of code slide(s)

      :return: None
    """
    if "code" in self.data:
      # Inline source code
      code = self.data["code"]
    else:
      try:
        # Source code in a file
        if self.data["file"][0] == "/":
          filename = (self.data["file"])
        elif self.data["file"][0] == "^":
          self.data["file"]= self.data["file"][1:]
          filename = self.data["file"]
        else:
          repository = os.getenv("DF_REPOSITORY")
          if repository == None :
            filename = self.slides_dir + "../" + self.data["file"]
          else:
            filename = repository + '/' + self.settings.EXTERNAL + \
              "/" + self.data["file"]

        fic = open(filename)
        code = fic.read()
      except:
        self.logger.critical("Unable to load the file %s in slide %s" %
          (self.data["file"], self.identifier))
        exit(6)

    # Syntax highlighting of the code
    if self.data.get("syntax", True):
      if "language" in self.data:
        lexer = pygments.lexers.get_lexer_by_name(self.data["language"],
            stripall = True)
      else:
        lexer = pygments.lexers.guess_lexer(code)
      self.data["source_code"] = pygments.highlight(code, lexer,
        pygments.formatters.HtmlFormatter())
    else:
      self.data["source_code"] = '<div class="highlight"><pre>' + \
        code + '</pre></div';
    
    code = self.data["source_code"].split("<pre>")
    lines = code[1].split("</pre>")[0].split("\n")
    # Delete the last line (empty line)
    lines.pop()
 
    # Add number of lines
    if self.data.get("linenumber", True):
      code = self.data["source_code"].split("<pre>")
      lines = code[1].split("</pre>")[0].split("\n")
      # Delete the last line (empty line)
      lines.pop()
      # Compute the number of caracters in the total number of lines
      digits = len(str(len(lines)))
      # Counter of lines
      cpt = 1
      for i in xrange(len(lines)):
        lines[i] = '<span class="linenumber">' + str(cpt).zfill(digits) + \
                       '. </span>' + lines[i]
        cpt += 1

    # If only parts of code selected
    if "lines" in self.data:
      tab_lines  = self.data["lines"].split(",")
      selected_lines = []
      for part in tab_lines:
        p = part.strip().split("-")
        if len(p) == 1:
          selected_lines.append(int(p[0]))
        else:
          selected_lines += range(int(p[0]), int(p[1]) + 1)
        # Insertion of "0" to delimit the portions by adding ...
        if part != tab_lines[len(tab_lines) - 1]:
          selected_lines.append(0)
      new_lines = [];
      for line in selected_lines:
        if line == 0:
          new_lines.append('<span class="linenumber">...</span>')
        else:
          new_lines.append(lines[line - 1])
      lines = new_lines
    # Explode multi lines codes
    size = len(lines)
    if size > 10:
      # Compute number of slides
      parts = size // 10
      if size % 10 != 0:
        parts += 1
      # Update of the max counter of progress bar
      if self.settings.CONSOLE_PROGRESS_BAR != None:
        self.settings.CONSOLE_PROGRESS_BAR.incMax(parts + 1)
        self.settings.CONSOLE_PROGRESS_BAR.incCurrent()
      multilines = [lines[ i * 10: (i + 1) * 10] 
                          for i in xrange(parts)]
      text = self.data["text"]
      for i in xrange(len(multilines)):
        multilines[i] = "\n".join(multilines[i])
        # Generate one slide for each group of code lines
        self.data["source_code"] = code[0] + "<pre>" + multilines[i] + \
            "</pre></div>"
        self.data["type"] = "multicode"
        if self.data.get("numberslide", False):
          self.data["text"] = "%s (%d/%d)" % (text, i + 1, parts)
        s = Slide(self.settings, self.data)
        # slide and report generation
        # self.settings.PROGRESS_BAR.decCurrent()
        s.generate_all(self.settings.REPORT_ACTIVATED)
    else:
      # Creation of string from lines code
      code[1] = "\n".join(lines)
      self.data["source_code"] = "<pre>".join(code) + "</pre></div>"
      self.data["type"] = "multicode"
      s = Slide(self.settings, self.data)
      # slide and report generation
      #self.settings.PROGRESS_BAR.decCurrent()
      if self.settings.CONSOLE_PROGRESS_BAR != None:
        self.settings.CONSOLE_PROGRESS_BAR.decCurrent()
      s.generate_all(self.settings.REPORT_ACTIVATED)
    
    self.settings.SLIDE -= 1



  def generate_external_slides(self):
    """
      Generation of the html code of the slide in the self.html attribute

      :return: None
    """
    filename = self.data['link'] + '.yaml'

    if filename[0] != '/' and filename[0] != '~':
      # Look in DF_REPOSITORY if the environment variable is defined
      repository = os.getenv("DF_REPOSITORY")
      if repository == None :
        filename = self.settings.DIR['presentation'] + '/' + filename
      elif filename[0] == "^":
        filename = filename[1:]
      else:
        filename_repos = repository + '/' + filename
        if not os.path.isfile(filename_repos):
          filename = self.settings.DIR['presentation'] + '/' + filename
        else:
          filename = repository + '/' + filename

    try:
      f = file(filename, "r")
    except IOError:
      self.logger.critical("No file %s found" % (filename,))
      exit(1)
 
    stream, length_stream = itertools.tee(yaml.load_all(f))

    self.settings.EXTERNAL = "/".join(self.data["link"].split("/")[:-1])

    for doc in stream:
      if "type" in doc:
        if doc["type"] == "external":
          self.logger.critical("Nested external type detected : only one " + 
            "level authorized")
          exit(7)
        elif doc["type"] != "cover":
          self.logger.info("Slide external detected")
          s = Slide(self.settings, doc)

          # slide and report generation
          s.generate_all(self.settings.REPORT_ACTIVATED)

    self.settings.SLIDE -= 1


  def generate_report(self):
    """
      Generation of the report page associated to the slide

      :return: LaTeX code of the report and True or,
               Dictionnary with data of the slide and False
      :rtype: (string|dictionnary, boolean)
    """
    hide_type = self.data.get("report", "")
    if hide_type == "hide" or self.data["type"] == "exercise_title":
      self.logger.info("Skipping slide screenshot for report : %s.png" %
        (self.identifier,))
      if self.settings.PREVIOUS_PAGE:
        #  return (pystache.render(self.template_report_unique,
         # self.settings.PREVIOUS_PAGE), True)
          return (self.settings.PREVIOUS_PAGE, False)
      else:
        return ("", True)
    else:
      # Screenshot of the slide if not exercise
      if self.data["type"] != "exercise":
        self.logger.info("Generating slide screenshot for report : %s.png" %
          (self.identifier,))
        os.system("phantomjs " + self.root_dir + "scripts/rasterize.js " +
          self.slides_dir + self.identifier + ".html?full#" + self.identifier +
          " " + self.report_dir + self.identifier + ".png")
      # Generate report page(s)
      if self.report_type == "1slide":
        return (pystache.render(self.template_report, 
              {"image1" : self.report_dir + "/%s" % (self.identifier,) }), True)
      elif self.report_type == "2slides":
        if not self.settings.PREVIOUS_PAGE:
          return ({"image1" : self.report_dir + "/%s" % (self.identifier,)},
              False)
        else:
          self.settings.PREVIOUS_PAGE['image2'] = self.report_dir + "/%s" % \
            (self.identifier,)
          return (pystache.render(self.template_report,
            self.settings.PREVIOUS_PAGE), True)
      elif self.report_type == "2slidesnnotes":
        # Detection of new page
        if self.data["type"] == "exercise" or hide_type == "hidescreen":
          newpage = ""
        else:
          newpage = r"\newpage" + "\n"

        # if detection of \chapter{ in notes add a flag
        if "notes" in self.data and self.data["notes"].find("\chapter{") != -1:
          self.data["chapter"] = True
        else:
          self.data["chapter"] = False

        if not self.settings.PREVIOUS_PAGE:
          if self.data["type"] == "exercise":
            return (pystache.render(self.template_report_exercise,
              {"title" : self.data["title"],
               "text" : self.data["text"]}), True)
          elif "notes" in self.data and hide_type == "hidescreen":
            return (newpage + pystache.render(self.template_report, 
              {"chapter" : self.data["chapter"],
               "notes"  : self.data["notes"]}), True)
          elif "notes" in self.data and hide_type != "hidenotes":
            return (newpage + pystache.render(self.template_report, 
              {"image1" : self.report_dir + "%s" % (self.identifier,),
               "chapter" : self.data["chapter"],
               "notes"  : self.data["notes"]}), True)
          else:
            return ({"image1" : self.report_dir + "%s" % (self.identifier,)},
              False)

        else:
          if "notes" in self.data and hide_type != "hidenotes":
            return ((newpage + pystache.render(self.template_report_unique,
              self.settings.PREVIOUS_PAGE), 
              newpage + pystache.render(self.template_report, 
              {"image1" : self.report_dir + "%s" % (self.identifier,),
               "chapter" : self.data["chapter"],
               "notes"  : self.data["notes"]})), True)
          else:
            self.settings.PREVIOUS_PAGE['image2'] = self.report_dir + "%s" % \
              (self.identifier,)
            return (newpage + pystache.render(self.template_report_2,
              self.settings.PREVIOUS_PAGE), True)


  def generate_all(self, report_activated):
    """
      Generation of the slide in html and the report page associated to 
      the slide

      :return: None
    """
    self.logger.info("Slide n." + str(self.settings.SLIDE))
    # Slide generation
    self.generate_slide()

    if self.html:
      # Save a screenshot of the slide
      self.save()

      # Create report page if needed
      if report_activated and self.external != self.identifier:
        report, final = self.generate_report()
        if final == True:
          if len(report) == 1:
            self.settings.REPORT["pages"] += report
          else:
            for i in range(len(report)):
              self.settings.REPORT["pages"] += report[i]
          self.settings.PREVIOUS_PAGE = {}
        else:
          if self.settings.PREVIOUS_PAGE:
            self.settings.PREVIOUS_PAGE.update(report)
          else:
            self.settings.PREVIOUS_PAGE = report

    self.settings.SLIDE += 1
