%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DownFall report template
%
% Original author : Mathias Legrand <legrand.mathias@gmail.com>
%
% Modified for DownFall : Tristan Colombo <tristan.colombo@info2dev.com> 
%                                         (@TristanColombo)
% Date   : 09-06-2013
% Last release : 09-17-2013
% DownFall report template is licensed under CC BY-NC-SA 3.0, see the file in
% the license directory for details.
%
% Compiling this template:
%
% 1) pdflatex main
% 2) makeindex main.idx
% 3) makeindex main.idx -s StyleIndex.ist
% 4) pdflatex main
%
% Images are stored in the images/ directory
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{df_report}

\LoadClass[11pt, fleqn]{book}

%%%%
% Variables
\newcommand{\theChapterImage}{}
\newcommand{\chapterImage}[1]{\renewcommand{\theChapterImage}{#1}}
% Default chapter image
\chapterImage{data/report/images/chapterHeader}

%%%%
% Page settings
\usepackage[a4paper, headsep=10pt, top=3cm, bottom=3cm, inner=3.2cm, 
            outer=2.2cm]{geometry}
\usepackage{fancyhdr}        % Simple header modification
\pagestyle{fancy}            % Activates the fancy header style 
\fancyhf{}                   % Deletes default header style

%%%%
% Font settings
% Use site http://www.tug.dk/FontCatalogue/ to select your fonts
\usepackage{microtype}       % Improves general appearance of text
\usepackage[utf8]{inputenc}  % Letters with accentuation
\usepackage[francais]{babel} % French hyphenation and translations
\usepackage{csquotes}        % French quotation marks
\usepackage[T1]{fontenc}     % T1 characters encoding
\usepackage{avant}           % Avant Garde font for headings
\usepackage{mathptmx}        % Times Roman as default font

%%%%
% Table of contents
\usepackage{titletoc}        % Easier table of contents manipulation
\usepackage[linktoc=all,hidelinks]{hyperref} % Hyperref links in table of
                                             % contents

%%%%
% Graphics
\usepackage{graphicx}        % Enables images inclusion
\graphicspath{{./images/}}   % Directory containing images to use
\usepackage{eso-pic}         % To add background image
\usepackage{tikz}            % To draw figures
\usepackage[framemethod=TikZ]{mdframed}     % To draw boxes
\usepackage{amssymb}         % Symboles
\usepackage{xcolor}          % Usage of colors
\definecolor{defaultColor}{rgb}{0, 0.56, 1} % Default color
\definecolor{black}{rgb}{0, 0, 0}           % Black color
\definecolor{exerciseColor}{rgb}{0, 0, 0}   % Exercise color
\definecolor{warningColor}{rgb}{1, 0, 0}    % Warning color
\definecolor{definitionColor}{rgb}{0.12, 0.17, 0.6} % Definition color
\definecolor{remarkColor}{rgb}{0.11, 0.81, 0.47}     % Remark color

%%%%
% Index
\usepackage{lettrine}        % Displays lettrines
\usepackage{makeidx}         % Index
\makeindex

%%%%
% Bibliography
%\usepackage[style=alphabetic,sorting=nyt,sortcites=true,autopunct=true,
%            babel=hyphen,hyperref=true,abbreviate=false,backref=true]{biblatex}
%\bibliography{bibliography} 
%\defbibheading{bibempty}{}

%%%%
% General
\usepackage{ifthen}
\usepackage{minted}          % Displays source code with syntax highlighting

%%%%
% Title Page text (used in \titlePage)
%  #1  : Title
%  #2  : Subtitle
%  #3  : Author
\newcommand{\titlePageText}[3]{
    \begingroup
        \thispagestyle{empty}
        \centering
        \vspace*{7.5cm}
        \par\fontsize{40}{20}
        \sffamily\selectfont
        % Title
        #1\par         
        \vspace*{0.5cm}
        % Subtitle
        {\Huge #2}\par        
        \vspace*{1cm}
        % Author
        {\LARGE #3}\par
    \endgroup
}

%%%%
% Title Page
% [#1] : Background image
%  #2  : Title
%  #3  : Subtitle
%  #4  : Author
%  #5  : Additional informations (leave blank if not needed)
\newcommand{\titlePage}[5][backgroundImage]{
    \begingroup
        % Background image
        \AddToShipoutPicture*{
            \put(0,0){\includegraphics[scale=1]{#1}}
        }
        % Text
        \titlePageText{#2}{#3}{#4}
    \endgroup

    \begingroup
        \newpage
        ~\vfill
        \thispagestyle{empty}
        % Title
        \noindent #2 - #3\\
        % Author
        \noindent #4\\
        % Additional informations 
        \ifthenelse{\equal{#5}{}}{
        }
        {
            \noindent #5\\
        }
    \endgroup

    \begingroup
        \newpage
        % Text
        \titlePageText{#2}{#3}{#4}
        \cleardoublepage
    \endgroup
}

%%%%
% Chapter header (\chapter)
\def\@makechapterhead#1{
    \thispagestyle{empty}
    {
        \begin{tikzpicture}[remember picture,overlay]
            \node at (current page.north west){
                \begin{tikzpicture}[remember picture,overlay]
                    \scalebox{0.7}
                    {
                        \node[anchor=north west,inner sep=0] at (5cm, -4cm){
                            \includegraphics[width=\paperwidth]{\theChapterImage}
                        };
                    }
                    \draw[anchor=west] (5cm,-13cm) node [rounded corners=25pt,
                    text opacity=1, draw=defaultColor, draw opacity=1,
                    line width=2pt, inner sep=15pt]{
                        \huge\sffamily\bfseries\textcolor{black}{
                            \thechapter\ ---\ #1\makebox[20cm]{}
                        }
                    };
                \end{tikzpicture}
            };
        \end{tikzpicture}
    }
    \par\vspace*{320pt}
    \normalfont
}

%%%%
% Chapter header (\chapter*) used for table of contents and index title
\def\@makeschapterhead#1{
    \thispagestyle{empty}
    {
        \begin{tikzpicture}[remember picture,overlay]
            \node at (current page.north west){
                \begin{tikzpicture}[remember picture,overlay]
                    \node[anchor=north west,inner sep=0] at (0, 0){
                        \includegraphics[width=\paperwidth]{\theChapterImage}
                    };
                    \draw[anchor=west] (5cm,-9cm) node [rounded corners=25pt,
                    fill=white, fill opacity=.6,
                    text opacity=1, draw=defaultColor, draw opacity=1,
                    line width=2pt, inner sep=15pt]{
                        \huge\sffamily\bfseries\textcolor{black}{
                            #1\makebox[20cm]{}
                        }
                    };
                \end{tikzpicture}
            };
        \end{tikzpicture}
    }
    \par\vspace*{230pt}
    \normalfont
}

%%%%
% Section header
\renewcommand{\@seccntformat}[1]{
    \llap{
        \textcolor{defaultColor}{\csname the#1\endcsname}
        \hspace{1em}
    }
}
\renewcommand{\section}{
    \@startsection{section}{1}{0pt}
    {-4ex \@plus -1ex \@minus -.4ex}
    {1ex \@plus .2ex }
    {\normalfont\large\sffamily\bfseries}
}
\renewcommand{\subsection}{
    \@startsection {subsection}{2}{0pt}
    {-3ex \@plus -0.1ex \@minus -.4ex}
    {0.5ex \@plus .2ex }
    {\normalfont\sffamily\bfseries}
}
\renewcommand{\subsubsection}{
    \@startsection {subsubsection}{3}{0pt}
    {-2ex \@plus -0.1ex \@minus -.2ex}
    {0.2ex \@plus .2ex }
    {\normalfont\small\sffamily\bfseries}}                        
\renewcommand{\paragraph}{
    \@startsection{paragraph}{4}{0pt}
    {-2ex \@plus -.2ex \@minus .2ex}
    {0.1ex}
    {\normalfont\small\sffamily\bfseries}
}

%%%%
% Header style
\renewcommand{\chaptermark}[1]{
    \markboth{\bsc{\chaptername~\thechapter{} :} #1}{}
} 
\renewcommand{\sectionmark}[1]{
    \markright{\thesection{} #1}
}
% Definition of the default header
\newcommand{\defineDefaultHeader}[0]{
    % Left header page
    \lhead[\sffamily\textbf{\textcolor{defaultColor}\thepage}]{
        \textsl{\rightmark}
    } 
    % Right header page
    \rhead[\textsl{\leftmark}]{
        \sffamily\textbf{\textcolor{defaultColor}\thepage}
    }
}
\defineDefaultHeader{}
% Clear style on even empty pages at end of chapters
\renewcommand{\cleardoublepage}{
    \clearpage
    \ifodd
        \c@page
    \else
        \hbox{}
        \vspace*{\fill}
        \thispagestyle{empty}
        \newpage
    \fi
}
% Space size between header and document body
\setlength{\headsep}{16pt}


%%%%
% Table of contents
% No margin
\contentsmargin{0cm} % Removes the default margin

% Chapter text style in table of contents
\titlecontents{chapter}[1.25cm]
{\addvspace{15pt}\large\sffamily\bfseries}
{\color{defaultColor!60}\contentslabel[\Large\thecontentslabel]{1.25cm}\color{defaultColor}}
{}  
{\color{defaultColor!60}\normalsize\sffamily\bfseries \titlerule*[.5pc]{.} \thecontentspage}

% Section text style in table of contents
\titlecontents{section}[1.25cm]
{\addvspace{5pt}\sffamily\bfseries}
{\contentslabel[\thecontentslabel]{1.25cm}}
{}
{\sffamily\hfill\color{black}\thecontentspage}

% Subsection text style in table of contents
\titlecontents{subsection}[1.25cm]
{\addvspace{1pt}\sffamily\small}
{\contentslabel[\thecontentslabel]{1.25cm}}
{}
{\sffamily\titlerule*[.5pc]{.} \thecontentspage}

%%%%
% \tableofcontents replacement
% [#1] : name of the image to display
\renewcommand{\tableofcontents}[1][]{
    % Left table of contents header page
    \lhead[\textbf{\textcolor{defaultColor}\thepage}]{
        \textsl{\contentsname}
    } 
    % Right table of contents header page
    \rhead[\textsl{\contentsname}]{
        \textbf{\textcolor{defaultColor}\thepage}
    }
    % Height header
    \setlength{\headheight}{14pt}
    % Initialize number of page to 1
    % Change style of number of page to roman for table of contents
    \pagenumbering{roman}
    \if@twocolumn
        \@restonecoltrue\onecolumn
    \else
        \@restonecolfalse
    \fi
    \ifthenelse{\equal{#1}{}}{
    }
    {
        \chapterImage{#1}
    }
 
    \chapter*{
        \contentsname
        \@mkboth{\MakeUppercase\contentsname}{\MakeUppercase\contentsname}
    }
    \@starttoc{toc}
    \if@restonecol
        \twocolumn
    \fi
    \cleardoublepage
    \pagestyle{fancy}
    % Initialize number of page to 1
    % Change style of number of page to arabic
    \pagenumbering{arabic}
    % Reactivation of default header
    \defineDefaultHeader{}
}

%%%%
% Index
% [#1] : name of the image to display
\newcommand{\displayIndex}[1][data/report/images/indexHeader]{
    \cleardoublepage
    \chapterImage{#1}
    \pagenumbering{gobble}
    \setlength{\columnsep}{0.75cm}
    \addcontentsline{toc}{chapter}{\textcolor{defaultColor}{\indexname}}
    \printindex
}

%%%%
% Bibliography
% [#1] : name of the image to display
%\newcommand{\displayBibliography}[1][]{
%    \cleardoublepage
%    \ifthenelse{\equal{#1}{}}{
%    }
%    {
%        \chapterImage{#1}
%    }
%    \chapter*{\bibname}
%    \addcontentsline{toc}{chapter}{\textcolor{defaultColor}{\bibname}} 
%    \printbibliography[heading=bibempty]
%}

%%%%
% Generic box definition
% [#1] : Color of the box
%  #2  : Name of the box
\newcommand{\defineBox}[2][defaultColor]{
    \newmdenv[
        backgroundcolor=#1!10,
        innerleftmargin=5pt,
        innerrightmargin=5pt,
        innertopmargin=5pt,
        innerbottommargin=5pt,
        leftmargin=0cm,
        rightmargin=0cm,
        linecolor=#1,
        outerlinewidth=.1pt,
        roundcorner=4pt,
        skipabove=\baselineskip,
        skipbelow=\baselineskip]{#2}

    \newmdenv[
        skipabove=7pt,
        skipbelow=7pt,
        rightline=false,
        leftline=true,
        topline=false,
        bottomline=false,
        backgroundcolor=#1!10,
        innerleftmargin=5pt,
        innerrightmargin=5pt,
        innertopmargin=5pt,
        innerbottommargin=5pt,
        leftmargin=0cm,
        rightmargin=0cm,
        linewidth=4pt,
        linecolor=#1,
        skipabove=\baselineskip,
        skipbelow=\baselineskip]{internal#2}
}

%%%%
% Environment box definition
% [#1] : Color of the box
%  #2  : Name of the environment
%  #3  : Label
%  #4  : Logo
%  #5  : Enable counter (true or false)
\newcommand{\defineEnvBox}[5][defaultColor]{
    \defineBox[#1]{box#2}
    \ifthenelse{\equal{#5}{true}}{
        \newcounter{c#2}
        \setcounter{c#2}{1}
    }
    {
    }
    \newenvironment{#2}{
        \vspace*{.5em}
        \begin{box#2}
            \vspace*{-1em}
            \includegraphics[width=1em]{#4}
            ~\\\textbf{#3}
            \ifthenelse{\equal{#5}{true}}{
                ~\textbf{\expandafter\csname thec#2\endcsname}
                \refstepcounter{c#2}
            }
            {}
            ~\vspace*{-1em}
            \begin{internalbox#2}
    }{
                \hfill{
                    \color{#1}\tiny\ensuremath{\blacksquare}
                }
            \end{internalbox#2}
        \end{box#2}
    }
}

%%%%
% Boxes environments
\defineEnvBox[black]{exercise}{Atelier}{data/report/images/icons/exercise}{true}
\defineEnvBox[remarkColor]{remark}{Remarque}{data/report/images/icons/remark}{false}
\defineEnvBox[definitionColor]{definition}{Définition}{data/report/images/icons/definition}{false}
\defineEnvBox[warningColor]{warning}{Attention !}{data/report/images/icons/warning}{false}
