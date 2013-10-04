# DownFall presentation system 

This is an HTML5 system build to create easily presentations and associated documents,
and update slides using a repository.

* Author : Tristan Colombo <[tristan.colombo@info2dev.com](mailto:tristan.colombo@info2dev.com?subject=DownFall)> ([@TristanColombo](http://twitter.com/TristanColombo)
* Date   : 09-05-2013
* Last release : 09-05-2013
* DownFall is licensed under [GNU GPL v3](http://www.gnu.org/licenses/gpl.html), see 
the file in the license directory for details.

* Actually only one core is proposed and it is based on Mozilla Evangelism Reps
  shower available on
  [https://github.com/mozilla-ro/presentations/tree/master/HTML5](https://github.com/mozilla-ro/presentations/tree/master/HTML5)
* Based on [@pepelsbey](http://twitter.com/pepelsbey)'s original shower system available on [https://github.com/pepelsbey/shower](https://github.com/pepelsbey/shower)
* Licensed under [MIT License](http://en.wikipedia.org/wiki/MIT_License), see [license page](https://github.com/pepelsbey/shower/wiki/License-En) for details.
* The technical documentation use the sphinx theme linfiniti by [Tim
  Sutton](mailto:tim@linfiniti.com) and licensed under Creative Commons By-SA, 
  see the file in the license directory 
  for details.


## How to install

* Download the source code
* Follow the directives in the INSTALL file

## How to use 

* Generate HTML files :
  downfall generate presentation.yaml
* Generate HTML files in quiet mode (progress bar and less verbose) :
  downfall generate --quiet presentation.yaml
* Generate HTML file and PDF document :
  downfall generate --report presentation.yaml
* Help on th downfall command :
  ** downfall --help
  ** downfall generate --help
* To test go in samples/demoYouWant and run :
  downfall generate -rq demoYouWant.yaml


## Contributing

You're always welcome to contribute. Fork project, make changes and send it as 
pull request. But it's better to file an [issue](https://github.com/df-project/downfall/issues) with your idea first and consult the [roadmap](https://github.com/df-project/downfall/ROADMAP.md).

---
Licensed under [GNU GPL v3](http://www.gnu.org/licenses/gpl.html), see 
the file in the license directory for details.

DownFall logo made by [Elisa de Castro Guerra](mailto:elisa@yemanjalisa.fr) and
licensed under [Free Art License 1.3](http://artlibre.org/licence/lal/en), see
the file in the license directory for details.
