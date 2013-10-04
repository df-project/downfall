# INSTALLATION Notes

## Using installer

On Debian based distribution you can simply execute :
sudo ./debian-installer.sh

On old distribution where TexLive 2012 is not available you can have
LaTeX errors. Do the following to solve the problem :
sudo apt-add-repository ppa:texlive-backports/ppa
sudo aptitude update
sudo aptitude safe-upgrade

## Manual install

Need libYAML :
==============
sudo aptitude install libyaml-0-2

Need nodejs, npm et phantomjs :
===============================
sudo aptitude install nodejs npm
sudo npm install -g phantomjs

Need LaTex TexLive > 2012 :
===========================
sudo aptitude install texlive texlive-latex3

Need pdflatex :
===============
sudo aptitude install texlive-latex-extra

Need biblatex :
===============
sudo aptitude install biblatex

Need mdframed :
===============
export TEXMFHOME=~/.texmf if not defined in ~/.bashrc
wget http://mirrors.ctan.org/macros/latex/contrib/mdframed.zip
unzip mdframed.zip
rm mdframed.zip
cd mdframed
make localinstall
cd ..
rm -R mdframed

Python dependencies are solved with :
=====================================
pip install -r requirements.txt

Environment variables (in ~/.bashrc if you use bash) :
======================================================
* DF_ROOT contains the path to the downfall directory :
  export DF_ROOT=/path/to/downfall
* DF_REPOSITORY contains the path to the repository of downfall's slides
  export DF_REPOSITORY=/path/to/DF_Repository
* Add $DF_ROOT/tools to your PATH :
  export PATH=$PATH:$DF_ROOT/tools

