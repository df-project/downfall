#!/bin/bash

###
#  Downfall Debian installer
#
#  Author: Tristan Colombo <tristan.colombo@info2dev.com>
#                          (@TristanColombo)
#
#  Date: 10-01-2013
#
#  Last modification: 10-01-2013
#
#  Licence: GNU GPL v3
###

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

DEPENDENCIES="libyaml-0-2 nodejs npm texlive texlive-latex3
texlive-latex-extra python python-pip"

USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)

USER_SHELL=`su -l $SUDO_USER -c "echo $SHELL"`
USER_SHELL=`echo $SHELL | cut -d/ -f3`

TEXMF=`su -l $SUDO_USER -c "cat /home/$SUDO_USER/.bashrc | grep TEXMFHOME | 
cut -d= -f2"`

DF_ROOT=`pwd`

DF_REPOSITORY="/home/"$SUDO_USER"/DF_REPOSITORY"

if [[ $USER_SHELL != "bash" ]]; then
  echo "This script work only for bash users" 1>&2
  exit 1
fi

echo "Installing dependencies..."
aptitude install $DEPENDENCIES

echo "Installing phantomjs script"
npm install -g phantomjs

echo "Installing Python modules dependencies"
pip install -r requirements.txt

echo "Installing mdframed class for LaTeX..."
if [[ $TEXMF != "" ]]; then
  echo "texmf directory detected in "$TEXMF
  TEXMF=`echo $USER_HOME$TEXMF | tr -d "~"`
else
  echo "export TEXMFHOME=~/.texmf" >> $USER_HOME/.bashrc
  TEXMF=$USER_HOME/.texmf
  if [ ! -d $TEXMF ]; then
    mkdir $TEXMF
    chown $SUDO_USER:$SUDO_USER $TEXMF
  fi
fi
wget http://mirrors.ctan.org/macros/latex/contrib/mdframed.zip
unzip mdframed.zip
rm mdframed.zip
cd mdframed
make localinstall
cd ..
rm -R mdframed
mv ~/texmf/* $TEXMF
chown -R $SUDO_USER:$SUDO_USER $TEXMF

#Environment variables
echo "DownFall root directory [$DF_ROOT]:"
read df
if [[ $df != "" ]]; then
  DF_ROOT=$df
fi
echo "export DF_ROOT=$DF_ROOT" >> $USER_HOME/.bashrc

echo "DownFall repository containing slides [$DF_REPOSITORY]:"
read df_repo
if [[ $df_repo != "" ]]; then
  DF_REPOSITORY=$df_repo
fi
echo "export DF_REPOSITORY=$DF_ROOT" >> $USER_HOME/.bashrc

echo "export PATH=\$PATH:\$DF_ROOT/tools" >> $USER_HOME/.bashrc
